"""
Build one day's tab for the "Nestilia Daily COGS" workbook from price_export.py output.

Usage (run in the folder holding nestilia_cogs_<day>.csv and nestilia_cogs_pct_<day>.csv):
    python3 build_day_tab.py <day> "<label>" <rate> <sheetId> "<rate source note>" "<export source note>" <prices.json> [notes]

Pass a 9th arg to also read order_notes.json ({"#N1463": "note"}) for extra Note text.
Writes rows_<day>.json (send with update_formulas to '<day>'!A1) and fmt_<day>.json
(batchUpdate: addSheet + formatting + notes, last request = sortRange by COGS %).
Send fmt without its last request first, then the rows, then the sortRange.
"""
import csv,json,sys
day,label,rate,sid,ratesrc,exportnote,prices_file=sys.argv[1:8]; rate=float(rate); sid=int(sid)
lines=list(csv.DictReader(open(f'nestilia_cogs_{day}.csv'))); orders=list(csv.DictReader(open(f'nestilia_cogs_pct_{day}.csv')))
prices=json.load(open(prices_file))
n=len(orders);o0=15;o1=o0+n-1;lt=o1+3;lh=lt+1;l0=lh+1;l1=l0+len(lines)-1
G=f'$G${l0}:$G${l1}';A=f'$A${l0}:$A${l1}'
rows=[[f'Nestilia COGS by order, {label}'],[f'Orders placed on {label} in store time (UTC+1), ranked by COGS %, highest first.'],[],['Inputs'],
['USD to EUR rate',rate,ratesrc],['Fallback share of selling price',0.33,'Used only when a product has no ticked Zendrop quote and no BER/PMs agent price'],[],['Day total'],
['Orders',f'=COUNTA(B{o0}:B{o1})'],['Paid (EUR)',f'=SUM(F{o0}:F{o1})'],['COGS (EUR)',f'=SUM(G{o0}:G{o1})'],['COGS %','=IF(B10=0,0,B11/B10)'],
['Orders above 50% COGS',f'=COUNTIF(H{o0}:H{o1},">0.5")'],['Rank','Order','Products','Fulfillment','Paid (USD)','Paid (EUR)','COGS (EUR)','COGS %','Gross profit (EUR)','Note']]
notes=json.load(open('order_notes.json')) if len(sys.argv)>8 else {}
for i,o in enumerate(orders):
    r=o0+i;note=[]
    if o['Discount code']: note.append(f"Discount code {o['Discount code']}")
    if o['Outstanding USD']: note.append(f"Unpaid balance ${float(o['Outstanding USD']):.2f}")
    if o['Uses 33% fallback']: note.append('Priced at 33% of selling price')
    if o['Order'] in notes: note.append(notes[o['Order']])
    rows.append([f'=RANK(H{r},$H${o0}:$H${o1})',o['Order'],o['Products'],o['Fulfillment'],float(o['Paid USD']),f'=E{r}*$B$5',f'=SUMIFS({G},{A},B{r})',f'=IF(F{r}=0,0,G{r}/F{r})',f'=F{r}-G{r}','; '.join(note) or None])
rows+=[[],[],['Order lines'],['Order','Product','Variant','Qty','Selling price (EUR)','Cost per offer (EUR)','COGS (EUR)','Source']]
fb=[]
for j,l in enumerate(lines):
    r=l0+j;p=prices[l['Product']]
    if 'sell_eur' in p: rows.append([l['Order'],l['Product'],l['Variant'],int(l['Qty (offers)']),p['sell_eur'],f'=$B$6*E{r}',f'=D{r}*F{r}',f"No quote in either sheet; 33% of selling price ({p['source']})"]);fb.append(r)
    else: rows.append([l['Order'],l['Product'],l['Variant'],int(l['Qty (offers)']),None,p['cost'],f'=D{r}*F{r}',p['source']])
rows=[(r+[None]*10)[:10] for r in rows]
json.dump(rows,open(f'rows_{day}.json','w'),ensure_ascii=False)
H=lambda h:{'red':round(int(h[1:3],16)/255,3),'green':round(int(h[3:5],16)/255,3),'blue':round(int(h[5:7],16)/255,3)}
gr=lambda a,b,c,d:{'sheetId':sid,'startRowIndex':a-1,'endRowIndex':b,'startColumnIndex':c,'endColumnIndex':d}
f=lambda a,b,c,d,u,fl:{'repeatCell':{'range':gr(a,b,c,d),'cell':{'userEnteredFormat':u},'fields':fl}}
EUR='"€"#,##0.00';tf='userEnteredFormat.textFormat';nf='userEnteredFormat.numberFormat'
hdr={'textFormat':{'bold':True,'foregroundColor':H('#FFFFFF')},'backgroundColor':H('#1F3864'),'wrapStrategy':'WRAP','verticalAlignment':'MIDDLE'}
hf=tf+'.bold,'+tf+'.foregroundColor,userEnteredFormat.backgroundColor,userEnteredFormat.wrapStrategy,userEnteredFormat.verticalAlignment'
bd={'style':'SOLID','colorStyle':{'rgbColor':H('#BFBFBF')}}
q=[{'addSheet':{'properties':{'sheetId':sid,'title':day,'index':sid}}},
 f(1,l1,0,10,{'textFormat':{'fontFamily':'Arial','fontSize':10}},tf+'.fontFamily,'+tf+'.fontSize'),
 f(1,1,0,1,{'textFormat':{'bold':True,'fontSize':14,'fontFamily':'Arial'}},tf),
 f(2,2,0,1,{'textFormat':{'italic':True,'fontFamily':'Arial','fontSize':10,'foregroundColor':H('#595959')}},tf),
 f(4,4,0,1,{'textFormat':{'bold':True,'fontFamily':'Arial','fontSize':10}},tf),f(8,8,0,1,{'textFormat':{'bold':True,'fontFamily':'Arial','fontSize':10}},tf),
 f(lt,lt,0,1,{'textFormat':{'bold':True,'fontFamily':'Arial','fontSize':12}},tf),
 f(5,6,1,2,{'textFormat':{'foregroundColor':H('#0000FF')}},tf+'.foregroundColor'),
 f(5,5,1,2,{'numberFormat':{'type':'NUMBER','pattern':'0.0000'}},nf),f(6,6,1,2,{'numberFormat':{'type':'PERCENT','pattern':'0%'}},nf),
 f(5,6,2,3,{'textFormat':{'italic':True,'foregroundColor':H('#595959'),'fontFamily':'Arial','fontSize':10}},tf),
 f(9,9,1,2,{'numberFormat':{'type':'NUMBER','pattern':'0'}},nf),f(13,13,1,2,{'numberFormat':{'type':'NUMBER','pattern':'0'}},nf),
 f(10,11,1,2,{'numberFormat':{'type':'CURRENCY','pattern':EUR}},nf),
 f(12,12,1,2,{'numberFormat':{'type':'PERCENT','pattern':'0.0%'},'textFormat':{'bold':True}},nf+','+tf+'.bold'),
 f(9,13,1,2,{'horizontalAlignment':'RIGHT'},'userEnteredFormat.horizontalAlignment'),
 f(14,14,0,10,hdr,hf),f(lh,lh,0,8,hdr,hf),
 f(o0,o1,0,1,{'horizontalAlignment':'CENTER','numberFormat':{'type':'NUMBER','pattern':'0'}},'userEnteredFormat.horizontalAlignment,'+nf),
 f(o0,o1,4,5,{'numberFormat':{'type':'CURRENCY','pattern':'"$"#,##0.00'}},nf),f(o0,o1,5,7,{'numberFormat':{'type':'CURRENCY','pattern':EUR}},nf),
 f(o0,o1,7,8,{'numberFormat':{'type':'PERCENT','pattern':'0.0%'},'textFormat':{'bold':True}},nf+','+tf+'.bold'),
 f(o0,o1,8,9,{'numberFormat':{'type':'CURRENCY','pattern':EUR+';-'+EUR}},nf),
 f(l0,l1,3,4,{'numberFormat':{'type':'NUMBER','pattern':'0'},'horizontalAlignment':'CENTER'},nf+',userEnteredFormat.horizontalAlignment'),
 f(l0,l1,4,7,{'numberFormat':{'type':'CURRENCY','pattern':EUR}},nf),f(l0,l1,4,6,{'textFormat':{'foregroundColor':H('#0000FF')}},tf+'.foregroundColor')]
q+=[f(r,r,5,6,{'textFormat':{'foregroundColor':H('#000000')}},tf+'.foregroundColor') for r in fb]
q+=[{'updateBorders':{'range':gr(a,b,0,c),'top':bd,'bottom':bd,'left':bd,'right':bd,'innerHorizontal':bd,'innerVertical':bd}} for a,b,c in [(14,o1,10),(lh,l1,8)]]
rg=[gr(o0,o1,7,8)]
q+=[{'addConditionalFormatRule':{'rule':{'ranges':rg,'booleanRule':{'condition':{'type':'NUMBER_GREATER_THAN_EQ','values':[{'userEnteredValue':'1'}]},'format':{'backgroundColor':H('#F4CCCC'),'textFormat':{'foregroundColor':H('#990000')}}}},'index':0}},
    {'addConditionalFormatRule':{'rule':{'ranges':rg,'booleanRule':{'condition':{'type':'NUMBER_GREATER','values':[{'userEnteredValue':'0.5'}]},'format':{'backgroundColor':H('#FCE5CD')}}},'index':1}}]
for a,b,w in [(0,1,110),(1,2,90),(2,3,230),(3,7,95),(7,8,80),(8,9,110),(9,10,260)]:
    q.append({'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'COLUMNS','startIndex':a,'endIndex':b},'properties':{'pixelSize':w},'fields':'pixelSize'}})
q.append({'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'ROWS','startIndex':13,'endIndex':14},'properties':{'pixelSize':36},'fields':'pixelSize'}})
q.append({'updateCells':{'rows':[{'values':[{'note':exportnote}]}],'fields':'note','start':{'sheetId':sid,'rowIndex':13,'columnIndex':0}}})
q.append({'updateCells':{'rows':[{'values':[{'note':"Cost per offer: ticked Nestilia rows of the Zendrop quote request sheet (US quote in EUR, column AH) first; otherwise BER/PMs sheet, USA tab, column H 'QP + 2,60' (agent price incl. the 2.60); otherwise 33% of the EUR selling price. Unticked Zendrop quotes are never used. COGS = Qty x cost per offer."}]}],'fields':'note','start':{'sheetId':sid,'rowIndex':lh-1,'columnIndex':0}}})
q.append({'sortRange':{'range':gr(o0,o1,0,10),'sortSpecs':[{'dimensionIndex':7,'sortOrder':'DESCENDING'}]}})
json.dump(q,open(f'fmt_{day}.json','w'),ensure_ascii=False)
print(o0,o1,l0,l1,fb,len(q))
