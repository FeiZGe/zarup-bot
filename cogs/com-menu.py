import discord
from discord.ext import commands

class ComMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot # เก็บ bot ไว้ใน view
    
    @discord.ui.button(label="พยากรณ์เรื่องร้องทุกข์", style=discord.ButtonStyle.primary)
    async def prophecyBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("พยากรณ์เรื่องร้องทุกข์", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)
    
    @discord.ui.button(label="ปัญหาที่พบบ่อย", style=discord.ButtonStyle.secondary)
    async def problemBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("ปัญหาที่พบบ่อย", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)

    @discord.ui.button(label="ประเมินการแก้ปัญหา", style=discord.ButtonStyle.green)
    async def evaluateBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("ประเมินการแก้ปัญหา", ephemeral=False)
        except Exception as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)

class ComMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="commenu", description="แสดงเมนูเรื่องร้องทุกข์")
    async def com_menu(self, ctx):
        view = ComMenu(self.bot)  # ส่ง bot ไปที่ view
        embed = discord.Embed(
            title="เมนูเรื่องร้องทุกข์",
            description="วิเคราะห์เรื่องร้องทุกข์ที่ประชาชนแจ้งเรื่องผ่าน 1111",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed, view=view)

# ฟังก์ชันสำหรับเพิ่ม Cog ให้กับ bot
def setup(bot):
    bot.add_cog(ComMenuCog(bot))