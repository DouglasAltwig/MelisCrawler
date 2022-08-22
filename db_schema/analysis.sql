-- CREATE INDEX idx_btree_seller_id ON public.items USING BTREE ((item_json -> 'seller' ->> 'id'));
-- CREATE INDEX idx_btree_seller_transactions_completed ON public.items USING BTREE ((item_json -> 'seller' -> 'seller_reputation' -> 'transactions' ->> 'completed'));
-- CREATE INDEX idx_btree_order_backend on public.items USING BTREE ((item_json->>'order_backend'));
-- CREATE INDEX idx_items ON public.items USING BTREE (site_id, item_id, last_run, category_id, (item_json->>'order_backend'));

-- SELECT * FROM public.items LIMIT 1;
-- SELECT DISTINCT ON(site_id, item_id, last_run, category_id, item_json ->> 'id') * FROM public.items LIMIT 10;

-- Informacoes uteis sobre os sellers
SELECT
item_json -> 'seller' ->> 'id' as seller_id,
item_json -> 'seller' ->> 'registration_date' as registration_date,
item_json -> 'seller' -> 'seller_reputation' ->> 'power_seller_status' as seller_status,
item_json -> 'seller' -> 'seller_reputation' ->> 'level_id' as seller_level,
item_json -> 'seller' -> 'seller_reputation' -> 'metrics' -> 'cancellations' ->> 'value' as cancellations_l60days,
item_json -> 'seller' -> 'seller_reputation' -> 'metrics' -> 'claims' ->> 'value' as claims_l60days,
item_json -> 'seller' -> 'seller_reputation' -> 'metrics' -> 'delayed_handling_time' ->> 'value' as delayed_handling_time_l60days,
item_json -> 'seller' -> 'seller_reputation' -> 'metrics' -> 'sales' ->> 'completed' as sales_completed_l60days,
item_json -> 'seller' -> 'seller_reputation' -> 'transactions' ->> 'canceled' as transactions_canceled_historic,
item_json -> 'seller' -> 'seller_reputation' -> 'transactions' ->> 'completed' as transactions_completed_historic,
item_json -> 'seller' -> 'seller_reputation' -> 'transactions' ->> 'total' as transactions_total_historic,
item_json -> 'seller' -> 'seller_reputation' -> 'transactions' -> 'ratings' ->> 'negative' as ratings_negative,
item_json -> 'seller' -> 'seller_reputation' -> 'transactions' -> 'ratings' ->> 'neutral' as ratings_neutral,
item_json -> 'seller' -> 'seller_reputation' -> 'transactions' -> 'ratings' ->> 'positive' as ratings_positive
FROM (SELECT DISTINCT ON(site_id, item_id, last_run, category_id, item_json ->> 'id') * FROM public.items) AS d
LIMIT 10;

-- Sellers mais bem avaliados do Mercado Livre cadastrados antes de 2021
SELECT 
	item_json -> 'seller' ->> 'id',
	AVG((item_json -> 'seller' -> 'seller_reputation' -> 'transactions' -> 'ratings' ->> 'positive')::decimal) as avg_positive
FROM (
	SELECT 
		DISTINCT ON (site_id, item_id, last_run, category_id) * 
	FROM public.items 
	WHERE item_json -> 'seller' ->> 'registration_date' < '2021-01-01'
	) as dist
GROUP BY (item_json -> 'seller' ->> 'id', item_json -> 'seller' -> 'seller_reputation' -> 'transactions' -> 'ratings' ->> 'positive')
ORDER BY avg_positive DESC
LIMIT 10;

-- Resultado da consulta
-- "seller_id"	"avg_positive"
-- "210618591"	1.00000000000000000000
-- "206838320"	1.00000000000000000000
-- "275089204"	1.00000000000000000000
-- "188439019"	1.00000000000000000000
-- "111592434"	1.00000000000000000000
-- "6657687"	1.00000000000000000000
-- "148123004"	1.00000000000000000000
-- "34864213"	1.00000000000000000000
-- "194743618"	1.00000000000000000000
-- "91837553"	1.00000000000000000000


-- Sellers que mais venderam no mercado livre no ultimos 60 dias
SELECT
	item_json -> 'seller' ->> 'id' as seller_id, 
	COUNT(item_json -> 'seller' -> 'seller_reputation' -> 'metrics' -> 'sales' ->> 'completed') as sales_completed_l60days
FROM (SELECT DISTINCT ON(site_id, item_id, last_run, category_id) * FROM public.items) as dist
GROUP BY (item_json -> 'seller' ->> 'id')
ORDER BY sales_completed_l60days DESC
LIMIT 10;

-- Resultado da consulta
-- "seller_id"	"sales_completed_l60days"
-- "219324699"	338138
-- "657293941"	184065
-- "652396705"	150066
-- "183589944"	136329
-- "727036761"	97095
-- "90723667"	87413
-- "255162860"	79683
-- "291206638"	71071
-- "193724256"	69728
-- "285668612"	64575


-- Produtos mais vendidos no Mercado Livre
SELECT 
item_json ->> 'id' as item_id,
item_json ->> 'title' as title,
item_json ->> 'price' as price,
item_json ->> 'available_quantity' as available_quantity,
(item_json ->> 'sold_quantity')::INTEGER as sold_quantity,
item_json -> 'seller' ->> 'id' as seller_id,
replace(item_json -> 'seller' ->> 'permalink', 'http://perfil.mercadolivre.com.br/', '') as seller_name
FROM (
	SELECT 
		DISTINCT ON (site_id, item_id, last_run, category_id) * 
	FROM public.items 
) as dist
ORDER BY sold_quantity DESC
LIMIT 100;

-- Resultado da consulta
-- "item_id"	"title"	"price"	"available_quantity"	"sold_quantity"	"seller_id"	"seller_name"
-- "MLB1392840081"	"Controle Longa Distancia Stetsom Sx2 Light Completo Colorido"	"55.71"	"500"	50000	"196540294"	"AUTOEQUIPBRASIL"
-- "MLB773008078"	"Tapete Tatame Eva 50x50x2cm 20mm"	"22.99"	"5000"	50000	"176350563"	"LOJADA+MARIA01"
-- "MLB1863576963"	"Ninho Instantâneo Forti+ Lata 380g"	"16.89"	"500"	50000	"742220069"	"NESTLE+STORES"
-- "MLB1863576963"	"Ninho Instantâneo Forti+ Lata 380g"	"21.8"	"500"	50000	"742220069"	"NESTLE+STORES"
-- "MLB1863576963"	"Ninho Instantâneo Forti+ Lata 380g"	"16.89"	"500"	50000	"742220069"	"NESTLE+STORES"
-- "MLB1965269525"	"Ultrapasse - Pagamento De Pedágios E Estacionamentos"	"14"	"5000"	50000	"797918371"	"VENDASULTRAPASSE"
-- "MLB981422074"	"Tatame Tapete Eva 1x1 10mm 100x100x1cm 1m²"	"41.39"	"5000"	50000	"145125631"	"LOJA+DAMARIA"
-- "MLB1863576963"	"Ninho Instantâneo Forti+ Lata 380g"	"21.8"	"500"	50000	"742220069"	"NESTLE+STORES"
-- "MLB1968534225"	"Lenço Umedecido Personalidade Baby C/100 Un"	"12.49"	"500"	50000	"502465500"	"DROG%C3%83O+NET"
-- "MLB1965269525"	"Ultrapasse - Pagamento De Pedágios E Estacionamentos"	"14"	"5000"	50000	"797918371"	"VENDASULTRAPASSE"
-- "MLB1968534225"	"Lenço Umedecido Personalidade Baby C/100 Un"	"11.99"	"500"	50000	"502465500"	"DROG%C3%83O+NET"
-- "MLB1968534225"	"Lenço Umedecido Personalidade Baby C/100 Un"	"11.99"	"500"	50000	"502465500"	"DROG%C3%83O+NET"
-- "MLB1392840081"	"Controle Longa Distancia Stetsom Sx2 Light Completo Colorido"	"55.71"	"500"	50000	"196540294"	"AUTOEQUIPBRASIL"
-- "MLB1489868685"	"Fórmula Infantil Em Pó Sem Glúten Danone Aptamil Premium 1  Em Lata De 800g - 0  A  6 Meses"	"52.9"	"1628"	26213	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1489868685"	"Fórmula Infantil Em Pó Sem Glúten Danone Aptamil Premium 1  Em Lata De 800g - 0  A  6 Meses"	"52"	"1718"	26061	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1489868685"	"Fórmula Infantil Em Pó Sem Glúten Danone Aptamil Premium 1  Em Lata De 800g - 0  A  6 Meses"	"49.03"	"291"	25718	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1503675678"	"Fórmula Infantil Em Pó Sem Glúten Danone Aptamil Premium 2  Em Lata De 800g - 6  A  10 Meses"	"52.9"	"769"	24173	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1503675678"	"Fórmula Infantil Em Pó Sem Glúten Danone Aptamil Premium 2  Em Lata De 800g - 6  A  10 Meses"	"49.3"	"1173"	23784	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1503675678"	"Fórmula Infantil Em Pó Sem Glúten Danone Aptamil Premium 2  Em Lata De 800g - 6  A  10 Meses"	"51.68"	"258"	23375	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1559396730"	"Fórmula Infantil Em Pó Sem Glúten Mead Johnson Enfagrow Composto Lácteo  Em Lata De 800g - 3  A 5 Anos"	"48.3"	"780"	21631	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1559396730"	"Fórmula Infantil Em Pó Sem Glúten Mead Johnson Enfagrow Composto Lácteo  Em Lata De 800g - 3  A 5 Anos"	"47"	"858"	21556	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2030464383"	"Toalha Umedecida Huggies Tripla Proteção 19cm X 14cm Pacote 96 Unidades"	"9.9"	"1049"	21272	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1454568133"	"Fórmula Infantil Em Pó Danone Aptamil Premium 3  Em Lata De 800g A Partir Dos 10 Meses"	"52.9"	"12"	20584	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2030464383"	"Toalha Umedecida Huggies Tripla Proteção 19cm X 14cm Pacote 96 Unidades"	"12.68"	"2773"	20066	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1739869766"	"Fórmula Infantil Em Pó Nestlé Nan Comfor 1  Em Lata De 800g - 0  A  6 Meses"	"59.1"	"549"	20001	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1454568133"	"Fórmula Infantil Em Pó Danone Aptamil Premium 3  Em Lata De 800g A Partir Dos 10 Meses"	"46.43"	"396"	19847	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1739869766"	"Fórmula Infantil Em Pó Nestlé Nan Comfor 1  Em Lata De 800g - 0  A  6 Meses"	"49.9"	"324"	19703	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1739869766"	"Fórmula Infantil Em Pó Nestlé Nan Comfor 1  Em Lata De 800g - 0  A  6 Meses"	"55.41"	"749"	19192	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1803038043"	"Fraldas Pampers Supersec M 30 U"	"33.49"	"6"	18101	"171551940"	"OURIMPORT"
-- "MLB1890691237"	"Fraldas Pampers Confort Sec Xg 58 U"	"98.69"	"115"	17647	"736159205"	"CIA+BRASILEIRA"
-- "MLB1890691237"	"Fraldas Pampers Confort Sec Xg 58 u"	"101.85"	"114"	17546	"736159205"	"CIA+BRASILEIRA"
-- "MLB2030412524"	"Creme Preventivo De Assaduras Sem Perfume Bepantol Baby Caixa 120g Grátis 20g Leve Mais Pague Menos"	"44.6"	"332"	15685	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1739874551"	"Fórmula Infantil Em Pó Nestlé Nan Comfort 2  Em Lata De 800g - 6  A  12 Meses"	"49.9"	"544"	15207	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1739874551"	"Fórmula Infantil Em Pó Nestlé Nan Comfort 2  Em Lata De 800g - 6  A  12 Meses"	"45.54"	"261"	14705	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1739874551"	"Fórmula Infantil Em Pó Nestlé Nan Comfort 2  Em Lata De 800g - 6  A  12 Meses"	"48.71"	"764"	14184	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1918231225"	"Toalhas Umedecidas Huggies Max Clean 48 U"	"18.9"	"2781"	12896	"480265022"	"MERCADOLIVRE+SUPERMERCADO"
-- "MLB1619908507"	"Fórmula Infantil Em Pó Nestlé Nan Comfor 3  Em Lata De 800g - 10 Meses 3 Anos"	"51.3"	"607"	12735	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1619908507"	"Fórmula Infantil Em Pó Nestlé Nan Comfor 3  Em Lata De 800g - 10 Meses 3 Anos"	"52"	"246"	12711	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1619908507"	"Fórmula Infantil Em Pó Nestlé Nan Comfor 3  Em Lata De 800g - 10 Meses 3 Anos"	"46.7"	"301"	12491	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1670034348"	"Pneu Pirelli P400 Evo P 175/65r14 82 H"	"367.1"	"800"	12423	"447822366"	"CARREFOUR.COM"
-- "MLB1670034348"	"Pneu Pirelli P400 Evo P 175/65r14 82 H"	"367.1"	"800"	12284	"447822366"	"CARREFOUR.COM"
-- "MLB2198690553"	"Som Automotivo Multilaser Trip P3350 Com Usb E Bluetooth"	"93.5"	"617"	12250	"1024303377"	"AUTO+EQUIPSC"
-- "MLB2198690553"	"Som Automotivo Multilaser Trip P3350 Com Usb E Bluetooth"	"93.5"	"637"	12169	"1024303377"	"AUTO+EQUIPSC"
-- "MLB2030438467"	"Fórmula Infantil Em Pó Sem Glúten Danone Milnutri Premium  Em Lata De 800g - 12 Meses 2 Anos"	"34.55"	"6"	11360	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2030438467"	"Fórmula Infantil Em Pó Sem Glúten Danone Milnutri Premium  Em Lata De 800g - 12 Meses 2 Anos"	"34.55"	"389"	11053	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1860026355"	"Fraldas Huggies Tripla Proteção G 36 U"	"35.66"	"152"	10901	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1860026355"	"Fraldas Huggies Tripla Proteção G 36 u"	"34.35"	"295"	10619	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1806510298"	"Fraldas Huggies Tripla Proteção Xg 66 U"	"91.22"	"37"	10618	"480265022"	"MERCADOLIVRE+SUPERMERCADO"
-- "MLB1806510298"	"Fraldas Huggies Tripla Proteção Xg 66 u"	"91.22"	"44"	10611	"480265022"	"MERCADOLIVRE+SUPERMERCADO"
-- "MLB1806510298"	"Fraldas Huggies Tripla Proteção Xg 66 u"	"91.22"	"44"	10611	"480265022"	"MERCADOLIVRE+SUPERMERCADO"
-- "MLB2030438467"	"Fórmula Infantil Em Pó Sem Glúten Danone Milnutri Premium  Em Lata De 800g - 12 Meses 2 Anos"	"35.28"	"11"	10593	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1803629273"	"Pneu Firestone F-series F-600 P 195/55r15 85 H"	"404.11"	"2269"	10326	"265786710"	"ACHEIPNEUS"
-- "MLB1621556496"	"Fórmula Infantil Em Pó Sem Glúten Nestlé Ninho Nutrigold  Em Lata De 800g A Partir Dos 12 Meses"	"41.88"	"60"	10062	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2029488559"	"Creme Preventivo De Assaduras Sem Perfume Bepantol Baby Caixa 120g Grátis 20g Leve Mais Pague Menos"	"39.9"	"212"	9972	"502465500"	"DROG%C3%83O+NET"
-- "MLB1860026355"	"Fraldas Huggies Tripla Proteção G 36 u"	"32.5"	"663"	9962	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1479197986"	"Fórmula Infantil Em Pó Sem Glúten Danone Aptamil Premium 1  Em Lata De 800g - 0  A  6 Meses"	"63.48"	"262"	9851	"502465500"	"DROG%C3%83O+NET"
-- "MLB1807880310"	"Fraldas Pampers Premium Care M 80 u"	"116.9"	"1"	9799	"577753856"	"WEB+MERCADINHO"
-- "MLB2029488559"	"Creme Preventivo De Assaduras Sem Perfume Bepantol Baby Caixa 120g Grátis 20g Leve Mais Pague Menos"	"37.8"	"140"	9619	"502465500"	"DROG%C3%83O+NET"
-- "MLB1740018027"	"Fórmula Infantil Em Pó Danone Aptamil Profutura 1  Em Lata De 800g - 0  A  6 Meses"	"59.53"	"201"	9413	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1855092707"	"Fraldas Pampers Confort Sec M 44 U"	"55.76"	"13"	9232	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1739886843"	"Fórmula Infantil Em Pó Nestlé Nan Supreme 2  Em Lata De 800g - 6  A  12 Meses"	"65.74"	"801"	9205	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2029488559"	"Creme Preventivo De Assaduras Sem Perfume Bepantol Baby Caixa 120g Grátis 20g Leve Mais Pague Menos"	"39.4"	"427"	9201	"502465500"	"DROG%C3%83O+NET"
-- "MLB1404143862"	"Pneu Kelly Edge Touring P 175/70r13 82 T"	"339.25"	"1000"	9178	"148815135"	"PNEUSTORE"
-- "MLB1739886843"	"Fórmula Infantil Em Pó Nestlé Nan Supreme 2  Em Lata De 800g - 6  A  12 Meses"	"67.45"	"406"	8973	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1739886843"	"Fórmula Infantil Em Pó Nestlé Nan Supreme 2  Em Lata De 800g - 6  A  12 Meses"	"69"	"172"	8826	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2002869267"	"Fralda Descartável Infantil Pampers Confort Sec Xxg Pacote 56 Unidades Leve Mais Pague Menos"	"98.69"	"345"	8818	"736159205"	"CIA+BRASILEIRA"
-- "MLB1404143862"	"Pneu Kelly Edge Touring P 175/70r13 82 T"	"339.25"	"992"	8730	"148815135"	"PNEUSTORE"
-- "MLB2014793271"	"Fraldas Huggies Supreme Care G 64 U"	"102.89"	"345"	8705	"736159205"	"CIA+BRASILEIRA"
-- "MLB2014793271"	"Fraldas Huggies Supreme Care G 64 u"	"94.49"	"121"	8684	"736159205"	"CIA+BRASILEIRA"
-- "MLB1739878405"	"Fórmula Infantil Em Pó Sem Glúten Nestlé Nan Supreme 1  Em Lata De 800g - 0  A  6 Meses"	"58.92"	"498"	8647	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2002869267"	"Fralda Descartável Infantil Pampers Confort Sec Xxg Pacote 56 Unidades Leve Mais Pague Menos"	"101.85"	"173"	8474	"736159205"	"CIA+BRASILEIRA"
-- "MLB1946451944"	"Fraldas Huggies Tripla Proteção Xg 32 U"	"32.46"	"41"	8430	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1739878405"	"Fórmula Infantil Em Pó Sem Glúten Nestlé Nan Supreme 1  Em Lata De 800g - 0  A  6 Meses"	"66.9"	"497"	8430	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2014793271"	"Fraldas Huggies Supreme Care G 64 u"	"94.49"	"338"	8293	"736159205"	"CIA+BRASILEIRA"
-- "MLB2002869368"	"Fralda Descartável Infantil Pampers Confort Sec G Pacote 60 Unidades"	"98.69"	"296"	8273	"736159205"	"CIA+BRASILEIRA"
-- "MLB1946451944"	"Fraldas Huggies Tripla Proteção Xg 32 u"	"32.46"	"58"	8260	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2065035464"	"Creme Preventivo De Assaduras Johnson & Johnson Desitin Caixa 113g Embalagem Econômica"	"49.55"	"1000"	8220	"179105330"	"LOJAONOFICIAL"
-- "MLB1739878405"	"Fórmula Infantil Em Pó Sem Glúten Nestlé Nan Supreme 1  Em Lata De 800g - 0  A  6 Meses"	"70.2"	"311"	8205	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2002869368"	"Fralda Descartável Infantil Pampers Confort Sec G Pacote 60 Unidades"	"95.92"	"240"	8165	"736159205"	"CIA+BRASILEIRA"
-- "MLB2065035464"	"Creme Preventivo De Assaduras Johnson & Johnson Desitin Caixa 113g Embalagem Econômica"	"41.93"	"1000"	8030	"179105330"	"LOJAONOFICIAL"
-- "MLB2060221147"	"Toalha Umedecida Huggies Tripla Proteção 19cm X 14cm Pacote 96 Unidades"	"12.99"	"11"	7955	"375051657"	"MUNDO+LELE"
-- "MLB1946451944"	"Fraldas Huggies Tripla Proteção Xg 32 u"	"32.51"	"96"	7898	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2002869368"	"Fralda Descartável Infantil Pampers Confort Sec G Pacote 60 Unidades"	"95.92"	"415"	7738	"736159205"	"CIA+BRASILEIRA"
-- "MLB2012685915"	"Fórmula Infantil Em Pó Mead Johnson Sustagen Kids Sabor Baunilha  Em Lata De 380g A Partir Dos 3 Anos"	"24.66"	"593"	7723	"502465500"	"DROG%C3%83O+NET"
-- "MLB2012685915"	"Fórmula Infantil Em Pó Mead Johnson Sustagen Kids Sabor Baunilha  Em Lata De 380g A Partir Dos 3 Anos"	"22.9"	"662"	7652	"502465500"	"DROG%C3%83O+NET"
-- "MLB2012685915"	"Fórmula Infantil Em Pó Mead Johnson Sustagen Kids Sabor Baunilha  Em Lata De 380g A Partir Dos 3 Anos"	"22"	"679"	7626	"502465500"	"DROG%C3%83O+NET"
-- "MLB2012685915"	"Fórmula Infantil Em Pó Mead Johnson Sustagen Kids Sabor Baunilha  Em Lata De 380g A Partir Dos 3 Anos"	"24.85"	"512"	7576	"502465500"	"DROG%C3%83O+NET"
-- "MLB1624387531"	"Fórmula Infantil Em Pó Nestlé Nestogeno 2  Em Lata De 800g - 6  A  12 Meses"	"38.89"	"212"	7422	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1624387531"	"Fórmula Infantil Em Pó Nestlé Nestogeno 2  Em Lata De 800g - 6  A  12 Meses"	"44.9"	"263"	7352	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1624387531"	"Fórmula Infantil Em Pó Nestlé Nestogeno 2  Em Lata De 800g - 6  A  12 Meses"	"42"	"297"	7313	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB1624387531"	"Fórmula Infantil Em Pó Nestlé Nestogeno 2  Em Lata De 800g - 6  A  12 Meses"	"45.31"	"445"	7182	"531132795"	"FERARIFOLEDROGARIALTDA"
-- "MLB2012698878"	"Fórmula Infantil Em Pó Mead Johnson Sustagen Kids Sabor Morango  Em Lata De 380g A Partir Dos 3 Anos"	"22.69"	"261"	7033	"502465500"	"DROG%C3%83O+NET"
-- "MLB1806621320"	"Fraldas Pampers Confort Sec M 80 U"	"87"	"453"	6958	"480265022"	"MERCADOLIVRE+SUPERMERCADO"
-- "MLB2012698878"	"Fórmula Infantil Em Pó Mead Johnson Sustagen Kids Sabor Morango  Em Lata De 380g A Partir Dos 3 Anos"	"22.9"	"422"	6866	"502465500"	"DROG%C3%83O+NET"
-- "MLB1806621320"	"Fraldas Pampers Confort Sec M 80 u"	"87"	"589"	6828	"480265022"	"MERCADOLIVRE+SUPERMERCADO"
-- "MLB2012698878"	"Fórmula Infantil Em Pó Mead Johnson Sustagen Kids Sabor Morango  Em Lata De 380g A Partir Dos 3 Anos"	"24.7"	"497"	6784	"502465500"	"DROG%C3%83O+NET"
-- "MLB2088103768"	"Som Automotivo First Option 8850b Com Usb, Bluetooth E Leitor De Cartão Sd"	"94"	"387"	6739	"15371897"	"AZACESSORIOS+MIX"
-- "MLB2012698878"	"Fórmula Infantil Em Pó Mead Johnson Sustagen Kids Sabor Morango  Em Lata De 380g A Partir Dos 3 Anos"	"22.78"	"507"	6652	"502465500"	"DROG%C3%83O+NET"
-- "MLB1831353518"	"Fraldas Huggies Supreme Care Recém-nascido Rn 34 U"	"26.49"	"1523"	6610	"480265022"	"MERCADOLIVRE+SUPERMERCADO"
-- "MLB2013139037"	"Fórmula Infantil Em Pó Nestlé Ninho Forti+ Instantâneo  Em Lata De 380g - 12 Meses 2 Anos"	"16.89"	"2562"	6543	"742220069"	"NESTLE+STORES"



-- MEBABO.COM
-- LOJA_EDIN
-- MACONEQUI
-- USEORGANICO
-- STARHOUSE
-- NENIS+COSMETICOS
-- EXTRA+FORMULAS
-- MERCARI+PERFUMES
-- KMG+STORE
-- IDEALONLINE
-- PHDERMA
-- 4CBOX
-- VITANUTRITION+OFICIAL
-- BRETZSAUDAVEIS
-- EBENASHOP
-- PERFUMARIA+EVAS
