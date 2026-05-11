import streamlit as st
# 從你的函式庫引入已經寫好的功能！名稱完全對應你的 Simulation_Fuction.py
from Simulation_Fuction import verify_draw, drawing

# ==========================================
# 1. 網頁基本設定
# ==========================================
st.set_page_config(page_title="機率驗證器", page_icon="🎲", layout="centered")
st.title("🎲 遊戲抽獎機率驗證系統")
st.write("透過統計學的假設檢定，科學驗證遊戲官方的抽獎機率是否屬實！")

# ==========================================
# 2. 側邊欄：設定通用參數
# ==========================================
with st.sidebar:
    st.header("⚙️ 基礎參數設定")
    
    # 對應變數: prob, significant_level, draw_times
    prob = st.number_input("官方機率 (例如 0.02 = 2%)", min_value=0.0001, max_value=1.0, value=0.02, step=0.01, format="%.4f")
    significant_level = st.slider("顯著水準 α", min_value=0.0001, max_value=0.1000, value=0.0500, step=0.0001, format="%.4f")
    draw_times = st.number_input("總抽獎次數", min_value=1, value=1000, step=10)
    
    st.info(f"💡 提示：顯著水準 α 越小 (例如 0.0001)，對「造假」的指控標準越嚴格，合理範圍會越寬。目前設定為 {significant_level:.4f}。")

# ==========================================
# 3. 建立共用的報告顯示函式 (避免重複寫程式碼)
# ==========================================
def display_report(result, sig_level, success_times):
    st.divider()
    st.subheader("📊 驗證報告")
    
    # 指標顯示板
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("期望中獎次數", f"{result['expected']:.0f} 次")
    col_b.metric("合理範圍下限", f"{result['range'][0]} 次")
    col_c.metric("合理範圍上限", f"{result['range'][1]} 次")
    
    st.caption(f"容許之 Z 分數範圍：(-{result['z_critical']:.3f} ~ {result['z_critical']:.3f}) / 實際 Z 分數：{result['z_score']:.3f}")
    
    # 結論判定
    if result['is_valid']:
        st.success(f"✅ **結論：在 α={sig_level} 測度下，實際中獎次數落入正常區間，判定機率【為真】。**")
    else:
        st.error(f"🚨 **警告：在 α={sig_level} 測度下，實際中獎次數異常，判定機率【為假】。**")
        
        # 幸運度評鑑 (非酋/歐皇警示)
        if success_times < result['range'][0]:
            st.warning(f"📉 **偏非警報**：低於合理下限，比預期最差情況還少中獎 **{result['range'][0] - success_times}** 次！")
        elif success_times > result['range'][1]:
            st.info(f"📈 **歐皇警報**：高於合理上限，比預期最好情況還多中獎 **{success_times - result['range'][1]}** 次！")

# ==========================================
# 4. 主畫面區域：利用頁籤切換模式
# ==========================================
tab_manual, tab_sim = st.tabs(["✍️ 手動輸入驗證", "🤖 機率模擬器驗證"])

# 模式 A：手動輸入
with tab_manual:
    st.subheader("手動輸入玩家數據")
    # 對應變數: success_times
    success_times_manual = st.number_input("實際中獎次數", min_value=0, value=15, step=1)
    
    if st.button("🚀 開始手動驗證", use_container_width=True):
        # 呼叫 verify_draw 函式
        result = verify_draw(n=draw_times, observed_success=success_times_manual, p=prob, alpha=significant_level)
        display_report(result, significant_level, success_times_manual)

# 模式 B：電腦自動模擬
with tab_sim:
    st.subheader("使用 Numpy 隨機產生抽獎樣本")
    st.write("系統將依照您設定的官方機率，自動跑完指定次數的抽獎，並直接對結果進行檢定。")
    
    if st.button("🎲 執行隨機模擬並驗證", use_container_width=True):
        with st.spinner("系統瘋狂抽卡中..."):
            # 呼叫 drawing 函式
            sim_bag = drawing(times=draw_times, prob=prob)
            success_times_sim = sim_bag.count("中獎")
            
        st.info(f"模擬完畢！本次電腦抽選之中獎率為：**{success_times_sim / draw_times:.4f}** (共中獎 {success_times_sim} 次)")
        
        # 呼叫 verify_draw 函式
        result = verify_draw(n=draw_times, observed_success=success_times_sim, p=prob, alpha=significant_level)
        display_report(result, significant_level, success_times_sim)