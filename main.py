import discord
from discord.ext import commands
import os
import json
from datetime import datetime
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv("TOKEN")
FILE_PESAN = "pesanan.json"
ADMIN_ID = 1422870723172765836 # ID MUHAMMAD RAMZY ALFARI

# ========== PRICELIST ROBUX KAMU ==========
PRODUK = {
    "robux": {
        "50_robux": 8500,
        "100_robux": 16500,
        "200_robux": 32500,
        "400_robux": 64000,
        "500_robux": 80000,
        "800_robux": 128000,
        "1000_robux": 160000,
        "1700_robux": 272000,
        "2000_robux": 250000,
        "3000_robux": 480000,
        "4500_robux": 7210000,
        "5000_robux": 8100000
    }
}

def load_json(file):
    if not os.path.exists(file): return {}
    with open(file, 'r') as f: return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f: json.dump(data, f, indent=4)

def generate_id():
    return f"NR{datetime.now().strftime('%d%m')}{random.randint(1000,9999)}"

@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} sudah online!')
    await bot.change_presence(activity=discord.Game(name="!menu | NR STORE ROBUX"))

@bot.command()
async def menu(ctx):
    embed = discord.Embed(title="🎮 NR STORE ROBUX", description="Jual Robux Termurah & Terpercaya 24 Jam", color=0x00ff00)
    embed.add_field(name="!list", value="Lihat daftar harga robux 50 - 5000", inline=False)
    embed.add_field(name="!order", value="`!order robux 400_robux UsernameRoblox`", inline=False)
    embed.add_field(name="!status", value="`!status ID_PESAN` Cek status pesanan", inline=False)
    embed.add_field(name="!bayar", value="`!bayar ID_PESAN` Konfirmasi sudah bayar", inline=False)
    embed.set_footer(text="⚠️ USERNAME JANGAN SAMPAI SALAH!")
    await ctx.send(embed=embed)

@bot.command()
async def list(ctx):
    embed = discord.Embed(title="📦 DAFTAR HARGA ROBUX NR STORE", color=0x0099ff, description="Harga bisa berubah sewaktu-waktu")
    txt = ""
    for item, harga in PRODUK["robux"].items():
        txt += f"`{item}` : **Rp {harga:,}**\n"
    embed.add_field(name="💎 ROBUX", value=txt, inline=False)
    embed.set_footer(text="Cara order:!order robux 800_robux UsernameKamu")
    await ctx.send(embed=embed)

@bot.command()
async def order(ctx, kategori: str, item: str, *, username_roblox: str):
    kategori = kategori.lower()
    item = item.lower()

    if kategori!= "robux":
        return await ctx.send("❌ Kategori cuma ada `robux`. Ketik `!list`")
    if item not in PRODUK["robux"]:
        return await ctx.send("❌ Paket tidak ada. Ketik `!list` buat liat paket 50-5000")

    harga = PRODUK["robux"][item]
    id_pesanan = generate_id()
    data = load_json(FILE_PESAN)

    data[id_pesanan] = {
        "user_id": ctx.author.id,
        "user_name": str(ctx.author),
        "kategori": kategori,
        "item": item,
        "target": username_roblox,
        "harga": harga,
        "status": "menunggu_pembayaran",
        "waktu": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_json(FILE_PESAN, data)

    embed = discord.Embed(title="🧾 INVOICE ROBUX NR STORE", color=0xffaa00)
    embed.add_field(name="ID Pesanan", value=f"`{id_pesanan}`", inline=False)
    embed.add_field(name="Produk", value=f"Robux - {item}", inline=True)
    embed.add_field(name="Username Roblox", value=username_roblox, inline=True)
    embed.add_field(name="Total Bayar", value=f"**Rp {harga:,}**", inline=False)
    embed.add_field(name="Metode Pembayaran", value="GOPAY: 083898005030\na.n Muhammad Ramzy Alfari", inline=False)
    embed.add_field(name="Catatan Penting", value="1. Wajib punya Gamepass di Roblox\n2. Ketik `!bayar {id_pesanan}` setelah transfer", inline=False)
    await ctx.send(f"{ctx.author.mention}", embed=embed)

@bot.command()
async def status(ctx, id_pesanan: str):
    data = load_json(FILE_PESAN)
    if id_pesanan not in data: return await ctx.send("❌ ID Pesanan tidak ditemukan")
    if data[id_pesanan]["user_id"]!= ctx.author.id: return await ctx.send("❌ Ini bukan pesanan kamu")

    status = data[id_pesanan]["status"]
    emoji = {"menunggu_pembayaran":"⏳", "menunggu_konfirmasi":"👀", "diproses":"⚙️", "selesai":"✅", "gagal":"❌"}
    embed = discord.Embed(title=f"Status: {status.upper()}", description=f"{emoji.get(status,'')} ID: {id_pesanan}", color=0x00ff00)
    embed.add_field(name="Produk", value=f"{data[id_pesanan]['item']}", inline=True)
    embed.add_field(name="Username", value=f"{data[id_pesanan]['target']}", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def bayar(ctx, id_pesanan: str):
    data = load_json(FILE_PESAN)
    if id_pesanan not in data: return await ctx.send("❌ ID Pesanan tidak ditemukan")
    if data[id_pesanan]["user_id"]!= ctx.author.id: return await ctx.send("❌ Ini bukan pesanan kamu")
    if data[id_pesanan]["status"]!= "menunggu_pembayaran": return await ctx.send("❌ Pesanan sudah dikonfirmasi")

    data[id_pesanan]["status"] = "menunggu_konfirmasi"
    save_json(FILE_PESAN, data)

    admin = await bot.fetch_user(ADMIN_ID)
    await admin.send(f"🔔 **NOTIF ADMIN NR STORE**\nOrder ROBUX BARU!\nID: `{id_pesanan}`\nUser: {ctx.author.mention}\nPaket: {data[id_pesanan]['item']}\nUsername: `{data[id_pesanan]['target']}`\nTotal: Rp {data[id_pesanan]['harga']:,}\nKetik `!proses {id_pesanan}`")
    await ctx.send("✅ Bukti pembayaran terkirim ke admin. Menunggu diproses 5-15 menit...")

@bot.command()
@commands.has_permissions(administrator=True)
async def proses(ctx, id_pesanan: str):
    data = load_json(FILE_PESAN)
    if id_pesanan not in data: return await ctx.send("❌ ID tidak ada")
    data[id_pesanan]["status"] = "diproses"
    save_json(FILE_PESAN, data)
    user = await bot.fetch_user(data[id_pesanan]["user_id"])
    await user.send(f"⚙️ Pesanan ROBUX `{id_pesanan}` sedang diproses. Mohon beli Gamepass atas nama bot ya!")
    await ctx.send(f"✅ Pesanan `{id_pesanan}` status: DIPROSES")

@bot.command()
@commands.has_permissions(administrator=True)
async def selesai(ctx, id_pesanan: str):
    data = load_json(FILE_PESAN)
    if id_pesanan not in data: return await ctx.send("❌ ID tidak ada")
    data[id_pesanan]["status"] = "selesai"
    save_json(FILE_PESAN, data)
    user = await bot.fetch_user(data[id_pesanan]["user_id"])
    await user.send(f"✅ Pesanan ROBUX `{id_pesanan}` SELESAI. Cek Robux nya ya! Terima kasih sudah order di NR STORE")
    await ctx.send(f"✅ Pesanan `{id_pesanan}` SELESAI")

@bot.command()
@commands.has_permissions(administrator=True)
async def pesanan(ctx):
    data = load_json(FILE_PESAN)
    if not data: return await ctx.send("Belum ada pesanan")
    txt = ""
    for idp, d in data.items():
        txt += f"`{idp}` | {d['status']} | {d['item']} | {d['target']}\n"
    embed = discord.Embed(title="📋 SEMUA PESAN ROBUX", description=txt, color=0x9932cc)
    await ctx.send(embed=embed)

bot.run(TOKEN)
