import discord
from discord.ext import commands

class URLInputModal(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title="กรอก URL")
        self.url_input = discord.ui.TextInput(
            label="URL ของบทความภาษาอังกฤษ", 
            style=discord.TextStyle.short,
            placeholder="กรอก URL ของคุณที่นี้...",
            required=True
        )
        self.add_item(self.url_input)
        self.bot = bot  # ให้ bot มีการกำหนด

    async def on_submit(self, interaction: discord.Interaction):
        try:
            url = self.url_input.value

            # ตรวจสอบว่า interaction ได้รับการตอบกลับหรือยัง
            if not interaction.response.is_done():
                # เรียกคำสั่ง summarize
                await self.bot.get_cog("SummarizeCog").summarize(interaction, url)  # ส่ง URL ไปยังคำสั่ง summarize
            else:
                print("Interaction already responded")

        except Exception as e:
            if not interaction.response.is_done():
                await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(f"An unexpected error occurred: {str(error)}", ephemeral=True)
            else:
                print(f"Error: {error}")

        except Exception as e:
            print(f"Error in error handler: {e}")

class Menu(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot  # เก็บ bot ไว้ใน view

    @discord.ui.button(label="สรุปบทความ", style=discord.ButtonStyle.primary)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            # เปิด modal ให้ผู้ใช้กรอก URL
            modal = URLInputModal(self.bot)  # ส่ง bot ไปที่ modal
            await interaction.response.send_modal(modal)
        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)

    @discord.ui.button(label="Button 2", style=discord.ButtonStyle.primary)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("Button 2 clicked", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)

class MenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="menu", description="แสดงเมนู")
    async def menu(self, ctx):
        view = Menu(self.bot)  # ส่ง bot ไปที่ view
        embed = discord.Embed(
            title="เมนู",
            description="สรุปบทความจาก URL",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, view=view)

# ฟังก์ชันสำหรับเพิ่ม Cog ให้กับ bot
async def setup(bot):
    await bot.add_cog(MenuCog(bot))