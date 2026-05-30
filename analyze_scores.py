import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd

# ==============================
# ファイルの読み込み
# ==============================
df2 = pd.read_csv("課題2.csv")
df3 = pd.read_csv("課題3.csv")

# ==============================
# 区切り線を表示するための関数
# ==============================
def print_separator(char="=", width=50):
    print(char * width)

def print_section(title):
    print_separator()
    print(f"  {title}")
    print_separator()


# ==============================
# 課題2の集計：参加者ごとの集計
# ==============================
print_section("課題2.csv ── 参加者ごとのスコア集計")
print()

# 参加者（名前）ごとにグループ化して集計
stats2 = df2.groupby("名前")["スコア"].agg(
    平均点="mean",
    最高点="max",
    最低点="min",
    受験科目数="count"
)

# 平均点を小数第1位に丸める
stats2["平均点"] = stats2["平均点"].round(1)

print(stats2.to_string())
print()

# 全体のトップ・ワースト
print("▼ 全体ランキング（平均点）")
ranking = stats2.sort_values("平均点", ascending=False)
for rank, (name, row) in enumerate(ranking.iterrows(), start=1):
    print(f"  {rank}位: {name}  平均 {row['平均点']} 点")

print()


# ==============================
# 課題3の集計：個人 & 所属部署ごと
# ==============================
print_section("課題3.csv ── 個人スコア一覧 & 部署別集計")
print()

# ── 個人スコア（降順） ──
print("▼ 個人スコア（高い順）")
df3_sorted = df3.sort_values("スコア", ascending=False).reset_index(drop=True)
df3_sorted.index += 1  # 1始まりに
print(df3_sorted.to_string())
print()

# ── 部署ごとの集計 ──
print("▼ 部署別集計")
stats3 = df3.groupby("所属")["スコア"].agg(
    平均点="mean",
    最高点="max",
    最低点="min",
    人数="count"
)
stats3["平均点"] = stats3["平均点"].round(1)
stats3_sorted = stats3.sort_values("平均点", ascending=False)
print(stats3_sorted.to_string())
print()

# ── 全体サマリー ──
print("▼ 全体サマリー（課題3）")
print(f"  参加者数 : {len(df3)} 人")
print(f"  全体平均 : {df3['スコア'].mean():.1f} 点")
print(f"  全体最高 : {df3['スコア'].max()} 点  ({df3.loc[df3['スコア'].idxmax(), '名前']})")
print(f"  全体最低 : {df3['スコア'].min()} 点  ({df3.loc[df3['スコア'].idxmin(), '名前']})")

print()
print_separator()
print("  集計完了！")
print_separator()
