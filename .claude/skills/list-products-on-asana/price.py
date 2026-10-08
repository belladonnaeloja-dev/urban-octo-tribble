import math,json,subprocess
def rates():
    try:
        out=subprocess.run(["curl","-sSL","-A","Mozilla/5.0","https://api.frankfurter.dev/v1/latest?base=EUR"],capture_output=True,text=True,timeout=30).stdout
        d=json.loads(out); r=d["rates"]; r["EUR"]=1.0; return r,d["date"]
    except Exception as e:
        return None,str(e)
def to_eur(amount,cur,r): return float(amount)/r[cur.upper()]
def nearest99(x):
    lo=math.floor(x)-0.01; hi=math.floor(x)+0.99
    return lo if abs(x-lo)<=abs(x-hi) else hi
def sell_price(amount,cur,r):
    """competitor price -> EUR -> minus 1 -> nearest xx.99"""
    return round(nearest99(to_eur(amount,cur,r)-1),2)
def offer_string(amount,cur,r,offer=None):
    p=f"{sell_price(amount,cur,r):.2f}"
    return f"{offer}: {p}" if offer else p
if __name__=="__main__":
    import sys
    r,d=rates(); print("rates date",d)
    for a in sys.argv[1:]:
        amt,cur=a.split(":")[:2]; off=a.split(":")[2] if a.count(":")>1 else None
        print(a,"->",offer_string(amt,cur,r,off))
