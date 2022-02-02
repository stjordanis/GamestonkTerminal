from datetime import datetime, timedelta
import os

import discordbot.config_discordbot as cfg
from discordbot.config_discordbot import logger
import disnake
import plotly.graph_objects as go
import yfinance as yf
from discordbot.helpers import autocrop_image
from PIL import Image
from plotly.subplots import make_subplots
import random


async def candle_command(
    ctx,
    ticker: str = "",
    interval: int = 15,
    start="",
    end="",
):
    """Shows candle plot of loaded ticker. [Source: Yahoo Finance, IEX Cloud or Alpha Vantage]

    Parameters
    ----------
    ticker: str
        Ticker name
    interval: int
        chart mins or daily
    start: str
        start date format YYYY-MM-DD
    end: str
        end date format YYYY-MM-DD
    """
    try:

        logger.info("candle %s %s %s %s", ticker, interval, start, end)

        if start == "":
            start = datetime.now() - timedelta(days=365)
        else:
            start = datetime.strptime(start, cfg.DATE_FORMAT)
        if end == "":
            end = datetime.now()
        else:
            end = datetime.strptime(end, cfg.DATE_FORMAT)

        futures = "=F"
        if interval == 1440:
            df_stock_candidate = yf.download(
                ticker,
                start=start,
                end=end,
                progress=False,
            )

            # Check that loading a stock was not successful
            if df_stock_candidate.empty:
                raise Exception(f"No data found for {ticker.upper()}")

            df_stock_candidate.index.name = "date"
        else:
            s_int = str(interval) + "m"
            d_granularity = {"1m": 1, "5m": 1, "15m": 1, "30m": 3, "60m": 3}
            s_start_dt = datetime.utcnow() - timedelta(days=d_granularity[s_int])
            s_date_start = s_start_dt.strftime("%Y-%m-%d")

            df_stock_candidate = yf.download(
                ticker,
                start=s_date_start
                if s_start_dt > start
                else start.strftime("%Y-%m-%d"),
                progress=False,
                interval=s_int,
                prepost=True,
            )

        # Check that loading a stock was not successful
        if df_stock_candidate.empty:
            raise Exception(f"No data found for {ticker.upper()}.")

        df_stock_candidate.index = df_stock_candidate.index.tz_localize(None)
        df_stock_candidate.index.name = "date"
        df_stock = df_stock_candidate

        plt_title = [f"{ticker.upper()} Intraday {interval}min", "Volume"]
        title = f"Intraday {interval}min Chart for {ticker.upper()}"
        if interval == 1440:
            plt_title = [f"{ticker.upper()} Daily", "Volume"]
            title = f"Daily Chart for {ticker.upper()}"

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.06,
            subplot_titles=plt_title,
            row_width=[0.2, 0.7],
        )
        fig.add_trace(
            go.Candlestick(
                x=df_stock.index,
                open=df_stock.Open,
                high=df_stock.High,
                low=df_stock.Low,
                close=df_stock.Close,
                name="OHLC",
            ),
            row=1,
            col=1,
        )
        colors = [
            "green" if row.Open < row["Adj Close"] else "red"
            for _, row in df_stock.iterrows()
        ]
        fig.add_trace(
            go.Bar(
                x=df_stock.index,
                y=df_stock.Volume,
                name="Volume",
                marker_color=colors,
            ),
            row=2,
            col=1,
        )
        fig.update_layout(
            margin=dict(l=0, r=0, t=25, b=5),
            template=cfg.PLT_CANDLE_STYLE_TEMPLATE,
            showlegend=False,
            yaxis_title="Stock Price ($)",
            yaxis=dict(
                fixedrange=False,
            ),
            xaxis=dict(
                rangeslider=dict(visible=False),
                type="date",
            ),
            dragmode="pan",
            hovermode="x unified",
        )
        fig.update_traces(xaxis="x1")
        if interval != 1440:
            if futures in ticker.upper():
                fig.update_xaxes(
                    rangebreaks=[
                        dict(bounds=["fri", "sun"]),
                        dict(bounds=[17, 17.5], pattern="hour"),
                    ],
                )
            else:
                fig.update_xaxes(
                    rangebreaks=[
                        dict(bounds=["sat", "mon"]),
                        dict(bounds=[19, 9.5], pattern="hour"),
                    ],
                )
        config = dict({"scrollZoom": True})
        imagefile = "candle.png"

        # Check if interactive settings are enabled
        plt_link = ""
        if cfg.INTERACTIVE:
            html_ran = random.randint(69, 69420)
            fig.write_html(f"in/candle_{html_ran}.html", config=config)
            plt_link = f"[Interactive]({cfg.INTERACTIVE_URL}/candle_{html_ran}.html)"

        fig.update_layout(
            width=800,
            height=500,
        )
        fig.write_image(imagefile)

        img = Image.open(imagefile)
        print(img.size)
        im_bg = Image.open(cfg.IMG_BG)
        h = img.height + 240
        w = img.width + 520

        # Paste fig onto background img and autocrop background
        img = img.resize((w, h), Image.ANTIALIAS)
        x1 = int(0.5 * im_bg.size[0]) - int(0.5 * img.size[0])
        y1 = int(0.5 * im_bg.size[1]) - int(0.5 * img.size[1])
        x2 = int(0.5 * im_bg.size[0]) + int(0.5 * img.size[0])
        y2 = int(0.5 * im_bg.size[1]) + int(0.5 * img.size[1])
        img = img.convert("RGB")
        im_bg.paste(img, box=(x1 - 5, y1, x2 - 5, y2))
        im_bg.save(imagefile, "PNG", quality=100)
        image = Image.open(imagefile)
        image = autocrop_image(image, 0)
        image.save(imagefile, "PNG", quality=100)

        image = disnake.File(imagefile)

        print(f"Image {imagefile}")
        embed = disnake.Embed(title=title, description=plt_link, colour=cfg.COLOR)
        embed.set_image(url=f"attachment://{imagefile}")
        embed.set_author(
            name=cfg.AUTHOR_NAME,
            icon_url=cfg.AUTHOR_ICON_URL,
        )
        os.remove(imagefile)

        await ctx.send(embed=embed, file=image)

    except Exception as e:
        embed = disnake.Embed(
            title="ERROR Stocks: Intraday",
            colour=cfg.COLOR,
            description=e,
        )

        await ctx.send(embed=embed, delete_after=30.0)
