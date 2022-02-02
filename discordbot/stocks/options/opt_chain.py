import os

import df2img
import discordbot.config_discordbot as cfg
import disnake
import numpy as np
import pandas as pd
from discordbot.config_discordbot import gst_imgur, logger
from discordbot.helpers import autocrop_image
from gamestonk_terminal.stocks.options import yfinance_model
from menus.menu import Menu
from PIL import Image


async def chain_command(
    ctx,
    ticker: str = None,
    expiry: str = None,
    opt_type: str = None,
    min_sp: float = None,
    max_sp: float = None,
):
    """Show calls/puts for given ticker and expiration"""
    try:
        # Debug
        if cfg.DEBUG:
            logger.debug(
                "opt-chain %s %s %s %s %s", ticker, expiry, opt_type, min_sp, max_sp
            )

        # Check for argument
        if not ticker:
            raise Exception("Stock ticker is required")

        dates = yfinance_model.option_expirations(ticker)

        if not dates:
            raise Exception("Stock ticker is invalid")

        options = yfinance_model.get_option_chain(ticker, expiry)
        calls_df = options.calls
        puts_df = options.puts

        column_map = {"openInterest": "oi", "volume": "vol", "impliedVolatility": "iv"}
        columns = [
            "strike",
            "bid",
            "ask",
            "volume",
            "openInterest",
            "impliedVolatility",
        ]

        if opt_type == "Calls":
            df = calls_df[columns].rename(columns=column_map)
        if opt_type == "Puts":
            df = puts_df[columns].rename(columns=column_map)

        min_strike = np.percentile(df["strike"], 1)
        max_strike = np.percentile(df["strike"], 100)

        if min_sp:
            min_strike = min_sp
        if max_sp:
            max_strike = max_sp
            if min_sp > max_sp:  # type: ignore
                min_sp, max_sp = max_strike, min_strike

        df = df[df["strike"] >= min_strike]
        df = df[df["strike"] <= max_strike]

        df["iv"] = pd.to_numeric(df["iv"].astype(float))

        formats = {"iv": "{:.2f}"}
        for col, f in formats.items():
            df[col] = df[col].map(lambda x: f.format(x))
        df.set_index("strike", inplace=True)

        title = f"Stocks: {opt_type} Option Chain for {ticker.upper()} on {expiry} [yfinance]"

        embeds: list = []
        # Weekly Calls Pages
        i, i2, end = 0, 0, 20
        df_pg = []
        embeds_img = []
        dindex = len(df.index)
        while i < dindex:
            df_pg = df.iloc[i:end]
            df_pg.append(df_pg)
            figp = df2img.plot_dataframe(
                df_pg,
                fig_size=(1000, (40 + (40 * 20))),
                col_width=[3, 3, 3, 3],
                tbl_cells=dict(
                    height=35,
                ),
                font=dict(
                    family="Consolas",
                    size=20,
                ),
                template="plotly_dark",
                paper_bgcolor="rgba(0, 0, 0, 0)",
            )
            imagefile = f"opt-chain{i}.png"

            df2img.save_dataframe(fig=figp, filename=imagefile)
            image = Image.open(imagefile)
            image = autocrop_image(image, 0)
            image.save(imagefile, "PNG", quality=100)

            uploaded_image = gst_imgur.upload_image(imagefile, title="something")
            image_link = uploaded_image.link
            embeds_img.append(
                f"{image_link}",
            )
            embeds.append(
                disnake.Embed(
                    title=title,
                    colour=cfg.COLOR,
                ),
            )
            i2 += 1
            i += 20
            end += 20
            os.remove(imagefile)

        # Author/Footer
        for i in range(0, i2):
            embeds[i].set_author(
                name=cfg.AUTHOR_NAME,
                url=cfg.AUTHOR_URL,
                icon_url=cfg.AUTHOR_ICON_URL,
            )
            embeds[i].set_footer(
                text=cfg.AUTHOR_NAME,
                icon_url=cfg.AUTHOR_ICON_URL,
            )

        i = 0
        for i in range(0, i2):
            embeds[i].set_image(url=embeds_img[i])

            i += 1
        embeds[0].set_footer(text=f"Page 1 of {len(embeds)}")
        options = [
            disnake.SelectOption(label="Home", value="0", emoji="🟢"),
        ]

        await ctx.send(embed=embeds[0], view=Menu(embeds, options))

    except Exception as e:
        embed = disnake.Embed(
            title="ERROR Stock-Options: Expirations",
            colour=cfg.COLOR,
            description=e,
        )
        embed.set_author(
            name=cfg.AUTHOR_NAME,
            icon_url=cfg.AUTHOR_ICON_URL,
        )
        await ctx.send(embed=embed, delete_after=30.0)
