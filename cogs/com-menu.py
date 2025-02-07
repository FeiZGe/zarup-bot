import discord
from discord.ext import commands
from utils.predata import load_data, problem_type
from utils.time_series import predict_future_complaints

# รายชื่อ 77 จังหวัดของไทย
THAI_PROVINCES = [
    "กรุงเทพมหานคร", "กระบี่", "กาญจนบุรี", "กาฬสินธุ์", "กำแพงเพชร", "ขอนแก่น", "จันทบุรี", "ฉะเชิงเทรา", 
    "ชลบุรี", "ชัยนาท", "ชัยภูมิ", "ชุมพร", "เชียงราย", "เชียงใหม่", "ตรัง", "ตราด", "ตาก", "นครนายก", 
    "นครปฐม", "นครพนม", "นครราชสีมา", "นครศรีธรรมราช", "นครสวรรค์", "นนทบุรี", "นราธิวาส", "น่าน", 
    "บึงกาฬ", "บุรีรัมย์", "ปทุมธานี", "ประจวบคีรีขันธ์", "ปราจีนบุรี", "ปัตตานี", "พระนครศรีอยุธยา", 
    "พังงา", "พัทลุง", "พิจิตร", "พิษณุโลก", "เพชรบุรี", "เพชรบูรณ์", "แพร่", "พะเยา", "ภูเก็ต", 
    "มหาสารคาม", "มุกดาหาร", "แม่ฮ่องสอน", "ยะลา", "ยโสธร", "ร้อยเอ็ด", "ระนอง", "ระยอง", "ราชบุรี", 
    "ลพบุรี", "ลำปาง", "ลำพูน", "ศรีสะเกษ", "สกลนคร", "สงขลา", "สตูล", "สมุทรปราการ", "สมุทรสงคราม", 
    "สมุทรสาคร", "สระแก้ว", "สระบุรี", "สิงห์บุรี", "สุโขทัย", "สุพรรณบุรี", "สุราษฎร์ธานี", "สุรินทร์", 
    "หนองคาย", "หนองบัวลำภู", "อ่างทอง", "อำนาจเจริญ", "อุดรธานี", "อุตรดิตถ์", "อุทัยธานี", "อุบลราชธานี"
]

class ComplaintDropdown(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.problem_type = None
        self.province = None

        # เพิ่ม Dropdown เข้าไปใน View ทันที
        self.add_item(self.ProblemTypeDropdown(self))
        self.add_item(self.ProvinceDropdown(self))

    async def get_selection(self):
        print(f"🟢 Debug: problem_type={self.problem_type}, province={self.province}")  # Debug
        return self.problem_type, self.province

    class ProblemTypeDropdown(discord.ui.Select):
        def __init__(self, parent_view):
            self.parent_view = parent_view
            options = [discord.SelectOption(label=ptype) for ptype in problem_type(load_data())]
            super().__init__(placeholder="เลือกประเภทปัญหา", options=options, max_values=1)

        async def callback(self, interaction: discord.Interaction):
            self.parent_view.problem_type = self.values[0]
            await interaction.response.edit_message(content=f"เลือกประเภทปัญหา: {self.parent_view.problem_type}")

    class ProvinceDropdown(discord.ui.Select):
        def __init__(self, parent_view):
            self.parent_view = parent_view
            options = [discord.SelectOption(label=prov) for prov in THAI_PROVINCES]
            super().__init__(placeholder="เลือกจังหวัด", options=options, max_values=1)

        async def callback(self, interaction: discord.Interaction):
            self.parent_view.province = self.values[0]
            await interaction.response.edit_message(content=f"เลือกจังหวัด: {self.parent_view.province}")

class ComMenu(discord.ui.View):
    def __init__(self, bot, dropdown):
        super().__init__()
        self.bot = bot
        self.dropdown = dropdown  # รับ dropdown เข้ามา

    @discord.ui.button(label="พยากรณ์เรื่องร้องทุกข์", style=discord.ButtonStyle.primary)
    async def predict_complaint(self, interaction: discord.Interaction, button: discord.ui.Button):
        problem_type, province = await self.dropdown.get_selection()
        if not problem_type or not province:
            await interaction.response.send_message("❌ กรุณาเลือกประเภทปัญหาและจังหวัดก่อน!", ephemeral=True)
            return
        try:
            data = load_data()
            prediction = predict_future_complaints(data, problem_type, province)
            await interaction.response.send_message(f"📊 พยากรณ์เรื่องร้องเรียนประเภท {problem_type} ใน {province}: {prediction}")
        except Exception as e:
            print(f"🔴 Error in predict_complaint: {e}")  # Debug Error
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

    @discord.ui.button(label="ปัญหาที่พบบ่อย", style=discord.ButtonStyle.secondary)
    async def problemBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("ปัญหาที่พบบ่อย", ephemeral=False)
        except Exception as e:
            print(f"🔴 Error in problemBtn: {e}")  # Debug Error
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

    @discord.ui.button(label="ประเมินการแก้ปัญหา", style=discord.ButtonStyle.green)
    async def evaluateBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("ประเมินการแก้ปัญหา", ephemeral=False)
        except Exception as e:
            print(f"🔴 Error in evaluateBtn: {e}")  # Debug Error
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

class ComMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="commenu", description="แสดงเมนูเรื่องร้องทุกข์")
    async def com_menu(self, ctx):
        try:
            print("🟢 คำสั่ง !commenu ถูกเรียกใช้งาน")  # Debug
            dropdown = ComplaintDropdown(self.bot)  # ✅ แก้ให้ `dropdown` อยู่ใน View ได้
            view = ComMenu(self.bot, dropdown)
            view.timeout = None  # ✅ ป้องกัน View หมดอายุ
            embed = discord.Embed(
                title="📢 เมนูเรื่องร้องทุกข์",
                description="เลือกประเภทปัญหาและจังหวัดเพื่อพยากรณ์จำนวนเรื่องร้องเรียน",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            print(f"🔴 Error in com_menu: {e}")  # Debug Error
            await ctx.send(f"❌ Error: {str(e)}")

# ฟังก์ชันสำหรับเพิ่ม Cog ให้กับ bot
async def setup(bot):
    await bot.add_cog(ComMenuCog(bot))
