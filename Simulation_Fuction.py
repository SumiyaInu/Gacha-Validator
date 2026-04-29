import random
import numpy as np
import math
from math import ceil,floor
import scipy.stats as stats


def drawing(times=None,prob=None):
    #抽選回数、ラインナップのデータと確率のデフォルト値
    probs =[prob,1-prob]
    if times is None:
        times = 100
    if probs is None:
        probs = [1-prob, prob]

    pool = ["中獎", "沒中獎"]

    bag=[]
    array_pool = np.array(pool)
    array_prob=np.array(probs)


    draw = np.random.choice(array_pool,size=times,replace=True,p=array_prob)
        #np.random.choice(抽選されるリストまたはマトリックス,size=(抽選人数,抽選回数),replace=重複できるかどうか（True=可，False=不可）,p=確率モジュール)
        #sizeに入った要素数により、生成された配列の次元数が異なります。この例では二次元配列になります
    bag.extend([str(item) for item in draw])  
        #ベクトル化したbagを一度リストにしてextendを執行する
        #extend:リストに全ての要素を追加する / append:1つずつに追加する
    
    return bag

def verify_draw(n, observed_success, p, alpha=0.05):
    """
    負責所有的統計計算，並回傳結果字典。
    """
    expected_val = n * p
    std_dev = math.sqrt(n * p * (1 - p))
    
    # 計算 Z 分數與門檻
    z_score = (observed_success - expected_val) / std_dev
    z_critical = stats.norm.ppf(1 - alpha/2)
    
    # 計算合理次數區間
    lower_bound = max(0, math.floor(expected_val - z_critical * std_dev))
    upper_bound = math.ceil(expected_val + z_critical * std_dev)
    
    # 判定
    is_valid = lower_bound <= observed_success <= upper_bound
    
    # 將所有結果包裝成字典回傳
    return {
        "is_valid": is_valid,
        "expected": expected_val,
        "range": (lower_bound, upper_bound),
        "z_score": z_score,
        "z_critical": z_critical,
        "diff": observed_success - expected_val
    }