import sys
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib

matplotlib.rcParams['font.family'] = 'Meiryo'

df2 = pd.read_csv("課題2.csv")
df3 = pd.read_csv("課題3.csv")

# ==============================
# 課題2 の可視化・分析
# ==============================
fig2, axes2 = plt.subplots(1, 3, figsize=(18, 6))
fig2.suptitle("課題2 ── 個人スコア分析", fontsize=16, fontweight="bold")

# ── グラフ1: 個人別平均点（棒グラフ）──
stats2 = df2.groupby("名前")["スコア"].agg(平均点="mean", 最高点="max", 最低点="min").round(1)
stats2_sorted = stats2.sort_values("平均点", ascending=True)

bars = axes2[0].barh(stats2_sorted.index, stats2_sorted["平均点"], color="steelblue", edgecolor="white")
axes2[0].set_xlabel("平均点")
axes2[0].set_title("個人別 平均点")
axes2[0].set_xlim(0, 100)
for bar, val in zip(bars, stats2_sorted["平均点"]):
    axes2[0].text(val + 0.5, bar.get_y() + bar.get_height() / 2,
                  f"{val}", va="center", fontsize=10)

# ── グラフ2: 日付別スコア推移（折れ線グラフ）──
df2["日付"] = pd.to_datetime(df2["日付"])
pivot = df2.groupby(["日付", "名前"])["スコア"].mean().unstack()
for name in pivot.columns:
    axes2[1].plot(pivot.index, pivot[name], marker="o", label=name)
axes2[1].set_xlabel("日付")
axes2[1].set_ylabel("平均スコア")
axes2[1].set_title("日付別 スコア推移")
axes2[1].legend(fontsize=8)
axes2[1].tick_params(axis="x", rotation=30)
axes2[1].set_ylim(50, 100)
axes2[1].grid(axis="y", linestyle="--", alpha=0.5)

# ── グラフ3: 科目別スコア分布（ボックスプロット）──
subjects = df2["科目"].unique()
data_by_subject = [df2[df2["科目"] == s]["スコア"].values for s in subjects]
bp = axes2[2].boxplot(data_by_subject, labels=subjects, patch_artist=True)
colors = ["#AED6F1", "#A9DFBF", "#F9E79F", "#F1948A", "#D7BDE2"]
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
axes2[2].set_ylabel("スコア")
axes2[2].set_title("科目別 スコア分布")
axes2[2].set_ylim(50, 100)
axes2[2].grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("課題2_分析グラフ.png", dpi=150, bbox_inches="tight")
print("課題2_分析グラフ.png を保存しました")
plt.close()

# ==============================
# 課題3 の可視化・分析
# ==============================
fig3, axes3 = plt.subplots(1, 3, figsize=(18, 6))
fig3.suptitle("課題3 ── 部署別スコア分析", fontsize=16, fontweight="bold")

dept_colors = {"開発": "#5DADE2", "管理": "#58D68D", "営業": "#F0B27A", "人事": "#C39BD3"}

# ── グラフ1: 部署別平均点（棒グラフ）──
stats3 = df3.groupby("所属")["スコア"].agg(平均点="mean", 最高点="max", 最低点="min", 人数="count").round(1)
stats3_sorted = stats3.sort_values("平均点", ascending=True)

bar_colors = [dept_colors.get(d, "gray") for d in stats3_sorted.index]
bars3 = axes3[0].barh(stats3_sorted.index, stats3_sorted["平均点"], color=bar_colors, edgecolor="white")
axes3[0].set_xlabel("平均点")
axes3[0].set_title("部署別 平均点")
axes3[0].set_xlim(70, 95)
for bar, val in zip(bars3, stats3_sorted["平均点"]):
    axes3[0].text(val + 0.2, bar.get_y() + bar.get_height() / 2,
                  f"{val}", va="center", fontsize=10)

# ── グラフ2: 部署別スコア分布（ボックスプロット）──
dept_order = stats3.sort_values("平均点", ascending=False).index.tolist()
data_by_dept = [df3[df3["所属"] == d]["スコア"].values for d in dept_order]
bp3 = axes3[1].boxplot(data_by_dept, labels=dept_order, patch_artist=True)
for patch, dept in zip(bp3["boxes"], dept_order):
    patch.set_facecolor(dept_colors.get(dept, "gray"))
axes3[1].set_ylabel("スコア")
axes3[1].set_title("部署別 スコア分布")
axes3[1].set_ylim(60, 100)
axes3[1].grid(axis="y", linestyle="--", alpha=0.5)

# ── グラフ3: 全体スコアのヒストグラム（部署色分け）──
for dept in dept_order:
    scores = df3[df3["所属"] == dept]["スコア"]
    axes3[2].hist(scores, bins=8, alpha=0.6, label=dept,
                  color=dept_colors.get(dept, "gray"), edgecolor="white")
axes3[2].axvline(df3["スコア"].mean(), color="red", linestyle="--", linewidth=1.5,
                 label=f"全体平均 {df3['スコア'].mean():.1f}")
axes3[2].set_xlabel("スコア")
axes3[2].set_ylabel("人数")
axes3[2].set_title("全体スコア分布（部署別）")
axes3[2].legend(fontsize=8)
axes3[2].grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("課題3_分析グラフ.png", dpi=150, bbox_inches="tight")
print("課題3_分析グラフ.png を保存しました")
plt.close()

# ==============================
# テキスト分析サマリー
# ==============================
print()
print("=" * 50)
print("  分析サマリー")
print("=" * 50)

print("\n【課題2】")
top2 = stats2.sort_values("平均点", ascending=False)
print(f"  最優秀者 : {top2.index[0]}（平均 {top2['平均点'].iloc[0]} 点）")
print(f"  最下位者 : {top2.index[-1]}（平均 {top2['平均点'].iloc[-1]} 点）")
print(f"  点差     : {top2['平均点'].iloc[0] - top2['平均点'].iloc[-1]:.1f} 点")
best_subject = df2.groupby("科目")["スコア"].mean().idxmax()
worst_subject = df2.groupby("科目")["スコア"].mean().idxmin()
print(f"  得意科目 : {best_subject}（全員平均 {df2.groupby('科目')['スコア'].mean()[best_subject]:.1f} 点）")
print(f"  苦手科目 : {worst_subject}（全員平均 {df2.groupby('科目')['スコア'].mean()[worst_subject]:.1f} 点）")

print("\n【課題3】")
top_dept = stats3["平均点"].idxmax()
low_dept = stats3["平均点"].idxmin()
print(f"  トップ部署 : {top_dept}（平均 {stats3.loc[top_dept, '平均点']} 点、{int(stats3.loc[top_dept, '人数'])} 人）")
print(f"  最下位部署: {low_dept}（平均 {stats3.loc[low_dept, '平均点']} 点、{int(stats3.loc[low_dept, '人数'])} 人）")
print(f"  全体平均  : {df3['スコア'].mean():.1f} 点")
print(f"  全体最高  : {df3['スコア'].max()} 点（{df3.loc[df3['スコア'].idxmax(), '名前']}）")
print(f"  全体最低  : {df3['スコア'].min()} 点（{df3.loc[df3['スコア'].idxmin(), '名前']}）")
above_avg = len(df3[df3["スコア"] >= df3["スコア"].mean()])
print(f"  平均以上  : {above_avg} 人 / {len(df3)} 人（{above_avg/len(df3)*100:.1f}%）")

print()
print("=" * 50)
print("  完了！")
print("=" * 50)
