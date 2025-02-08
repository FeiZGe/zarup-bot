import os
import discord
from discord.ext import commands
from utils.predata import load_data
from utils.time_series import predict_future_complaints

class ComplaintModal(discord.ui.Modal, title="🔍 พยากรณ์เรื่องร้องทุกข์"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.add_item(discord.ui.TextInput(label="ประเภทปัญหา", placeholder="เช่น การจราจร, ภัยธรรมชาติ"))
        self.add_item(discord.ui.TextInput(label="จังหวัด", placeholder="กรอกชื่อจังหวัด (เช่น กรุงเทพมหานคร)"))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            problem_type = self.children[0].value.strip()
            province = self.children[1].value.strip()
            
            if not problem_type or not province:
                await interaction.response.send_message("❌ กรุณากรอกข้อมูลให้ครบถ้วน", ephemeral=True)
                return

            data = load_data()
            prediction, graph_path = predict_future_complaints(data, problem_type, province)

            if prediction is None or graph_path is None:
                await interaction.response.send_message("❌ ไม่สามารถพยากรณ์ข้อมูลได้ กรุณาตรวจสอบข้อมูลอีกครั้ง", ephemeral=True)
                return

            # ✅ สร้าง Embed
            embed = discord.Embed(
                title="📊 ผลการพยากรณ์เรื่องร้องเรียนในปีหน้า",
                description=f"🔹 ประเภทปัญหา: **{problem_type}**\n🔹 จังหวัด: **{province}**\n📌 จำนวนที่คาดการณ์: **{prediction}**",
                color=discord.Color.yellow()
            )

            # ✅ ตรวจสอบว่ามีรูปในโฟลเดอร์ `assets/graphs` หรือไม่
            if not os.path.exists(graph_path):
                await interaction.response.send_message("❌ ไม่พบไฟล์ภาพกราฟ กรุณาลองใหม่อีกครั้ง", ephemeral=True)
                return

            # ✅ ส่ง Embed + รูปกราฟไปยัง DM
            user = interaction.user
            try:
                await user.send(embed=embed)
                await user.send(file=discord.File(graph_path))
                await interaction.response.send_message("📩 **ผลลัพธ์ถูกส่งไปยัง DM ของคุณแล้ว**", ephemeral=True, delete_after=5)
            except discord.Forbidden:
                await interaction.response.send_message("❌ **ไม่สามารถส่ง DM ได้** กรุณาเปิดการรับข้อความจากเซิร์ฟเวอร์!", ephemeral=True, delete_after=5)

        except Exception as e:
            print(f"🔴 Error in ComplaintModal: {e}")
            await interaction.response.send_message(f"❌ เกิดข้อผิดพลาด: {e}", ephemeral=True)

class ComMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="พยากรณ์เรื่องร้องทุกข์", style=discord.ButtonStyle.primary)
    async def predict_complaint(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(ComplaintModal(self.bot))  # เปิด Modal
        except Exception as e:
            print(f"🔴 Error in predict_complaint: {e}")
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

    @discord.ui.button(label="ปัญหาที่พบบ่อย", style=discord.ButtonStyle.secondary)
    async def problemBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("📌 ปัญหาที่พบบ่อย: (รอข้อมูล)", ephemeral=False)
        except Exception as e:
            print(f"🔴 Error in problemBtn: {e}")
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

    @discord.ui.button(label="ประเมินการแก้ปัญหา", style=discord.ButtonStyle.green)
    async def evaluateBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("💬 ประเมินการแก้ปัญหา: (รอข้อมูล)", ephemeral=False)
        except Exception as e:
            print(f"🔴 Error in evaluateBtn: {e}")
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

class ComMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="commenu", description="แสดงเมนูเรื่องร้องทุกข์")
    async def com_menu(self, ctx):
        try:
            print("🟢 คำสั่ง !commenu ถูกเรียกใช้งาน")
            view = ComMenu(self.bot)
            embed = discord.Embed(
                title="📢 เมนูเรื่องร้องทุกข์",
                description="กรอกข้อมูลเพื่อพยากรณ์จำนวนเรื่องร้องเรียน",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            print(f"🔴 Error in com_menu: {e}")
            await ctx.send(f"❌ Error: {str(e)}")

# ฟังก์ชันสำหรับเพิ่ม Cog ให้กับ bot
async def setup(bot):
    await bot.add_cog(ComMenuCog(bot))
