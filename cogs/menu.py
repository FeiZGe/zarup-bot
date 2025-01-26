import discord
from discord.ext import commands

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Button 1", style=discord.ButtonStyle.primary)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("Button 1 clicked", ephemeral=False)
        except Exception as e:
            await print(f"Error: {str(e)}")

    @discord.ui.button(label="Button 2", style=discord.ButtonStyle.primary)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("Button 2 clicked", ephemeral=False)
        except Exception as e:
            await print(f"Error: {str(e)}")


class MenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="menu", description="แสดงเมนู")
    async def menu(self, ctx):
        view = Menu()
        embed = discord.Embed(
            title="เมนู",
            description="สรุปบทความจาก URL",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, view=view)

# ฟังก์ชันสำหรับเพิ่ม Cog ให้กับ bot
async def setup(bot):
    await bot.add_cog(MenuCog(bot))