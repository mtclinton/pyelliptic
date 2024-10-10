import pytest
import binascii

from pyelliptic.elliptic import CurveParams
from pyelliptic.elliptic import generate_key, marshall, unmarshall

p384_test_data = [
    {
        "k": "1",
        "x": "AA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A385502F25DBF55296C3A545E3872760AB7",
        "y": "3617DE4A96262C6F5D9E98BF9292DC29F8F41DBD289A147CE9DA3113B5F0B8C00A60B1CE1D7E819D7A431D7C90EA0E5F",
    },
    {
        "k": "2",
        "x": "08D999057BA3D2D969260045C55B97F089025959A6F434D651D207D19FB96E9E4FE0E86EBE0E64F85B96A9C75295DF61",
        "y": "8E80F1FA5B1B3CEDB7BFE8DFFD6DBA74B275D875BC6CC43E904E505F256AB4255FFD43E94D39E22D61501E700A940E80",
    },
    {
        "k": "3",
        "x": "077A41D4606FFA1464793C7E5FDC7D98CB9D3910202DCD06BEA4F240D3566DA6B408BBAE5026580D02D7E5C70500C831",
        "y": "C995F7CA0B0C42837D0BBE9602A9FC998520B41C85115AA5F7684C0EDC111EACC24ABD6BE4B5D298B65F28600A2F1DF1",
    },
    {
        "k": "4",
        "x": "138251CD52AC9298C1C8AAD977321DEB97E709BD0B4CA0ACA55DC8AD51DCFC9D1589A1597E3A5120E1EFD631C63E1835",
        "y": "CACAE29869A62E1631E8A28181AB56616DC45D918ABC09F3AB0E63CF792AA4DCED7387BE37BBA569549F1C02B270ED67",
    },
    {
        "k": "5",
        "x": "11DE24A2C251C777573CAC5EA025E467F208E51DBFF98FC54F6661CBE56583B037882F4A1CA297E60ABCDBC3836D84BC",
        "y": "8FA696C77440F92D0F5837E90A00E7C5284B447754D5DEE88C986533B6901AEB3177686D0AE8FB33184414ABE6C1713A",
    },
    {
        "k": "6",
        "x": "627BE1ACD064D2B2226FE0D26F2D15D3C33EBCBB7F0F5DA51CBD41F26257383021317D7202FF30E50937F0854E35C5DF",
        "y": "09766A4CB3F8B1C21BE6DDA6C14F1575B2C95352644F774C99864F613715441604C45B8D84E165311733A408D3F0F934",
    },
    {
        "k": "7",
        "x": "283C1D7365CE4788F29F8EBF234EDFFEAD6FE997FBEA5FFA2D58CC9DFA7B1C508B05526F55B9EBB2040F05B48FB6D0E1",
        "y": "9475C99061E41B88BA52EFDB8C1690471A61D867ED799729D9C92CD01DBD225630D84EDE32A78F9E64664CDAC512EF8C",
    },
    {
        "k": "8",
        "x": "1692778EA596E0BE75114297A6FA383445BF227FBE58190A900C3C73256F11FB5A3258D6F403D5ECE6E9B269D822C87D",
        "y": "DCD2365700D4106A835388BA3DB8FD0E22554ADC6D521CD4BD1C30C2EC0EEC196BADE1E9CDD1708D6F6ABFA4022B0AD2",
    },
    {
        "k": "9",
        "x": "8F0A39A4049BCB3EF1BF29B8B025B78F2216F7291E6FD3BAC6CB1EE285FB6E21C388528BFEE2B9535C55E4461079118B",
        "y": "62C77E1438B601D6452C4A5322C3A9799A9B3D7CA3C400C6B7678854AED9B3029E743EFEDFD51B68262DA4F9AC664AF8",
    },
    {
        "k": "10",
        "x": "A669C5563BD67EEC678D29D6EF4FDE864F372D90B79B9E88931D5C29291238CCED8E85AB507BF91AA9CB2D13186658FB",
        "y": "A988B72AE7C1279F22D9083DB5F0ECDDF70119550C183C31C502DF78C3B705A8296D8195248288D997784F6AB73A21DD",
    },
    {
        "k": "11",
        "x": "099056E27DA7B998DA1EEEC2904816C57FE935ED5837C37456C9FD14892D3F8C4749B66E3AFB81D626356F3B55B4DDD8",
        "y": "2E4C0C234E30AB96688505544AC5E0396FC4EED8DFC363FD43FF93F41B52A3255466D51263AAFF357D5DBA8138C5E0BB",
    },
    {
        "k": "12",
        "x": "952A7A349BD49289AB3AC421DCF683D08C2ED5E41F6D0E21648AF2691A481406DA4A5E22DA817CB466DA2EA77D2A7022",
        "y": "A0320FAF84B5BC0563052DEAE6F66F2E09FB8036CE18A0EBB9028B096196B50D031AA64589743E229EF6BACCE21BD16E",
    },
    {
        "k": "13",
        "x": "A567BA97B67AEA5BAFDAF5002FFCC6AB9632BFF9F01F873F6267BCD1F0F11C139EE5F441ABD99F1BAAF1CA1E3B5CBCE7",
        "y": "DE1B38B3989F3318644E4147AF164ECC5185595046932EC086329BE057857D66776BCB8272218A7D6423A12736F429CC",
    },
    {
        "k": "14",
        "x": "E8C8F94D44FBC2396BBEAC481B89D2B0877B1DFFD23E7DC95DE541EB651CCA2C41ABA24DBC02DE6637209ACCF0F59EA0",
        "y": "891AE44356FC8AE0932BCBF6DE52C8A933B86191E7728D79C8319413A09D0F48FC468BA05509DE22D7EE5C9E1B67B888",
    },
    {
        "k": "15",
        "x": "B3D13FC8B32B01058CC15C11D813525522A94156FFF01C205B21F9F7DA7C4E9CA849557A10B6383B4B88701A9606860B",
        "y": "152919E7DF9162A61B049B2536164B1BEEBAC4A11D749AF484D1114373DFBFD9838D24F8B284AF50985D588D33F7BD62",
    },
    {
        "k": "16",
        "x": "D5D89C3B5282369C5FBD88E2B231511A6B80DFF0E5152CF6A464FA9428A8583BAC8EBC773D157811A462B892401DAFCF",
        "y": "D815229DE12906D241816D5E9A9448F1D41D4FC40E2A3BDB9CABA57E440A7ABAD1210CB8F49BF2236822B755EBAB3673",
    },
    {
        "k": "17",
        "x": "4099952208B4889600A5EBBCB13E1A32692BEFB0733B41E6DCC614E42E5805F817012A991AF1F486CAF3A9ADD9FFCC03",
        "y": "5ECF94777833059839474594AF603598163AD3F8008AD0CD9B797D277F2388B304DA4D2FAA9680ECFA650EF5E23B09A0",
    },
    {
        "k": "18",
        "x": "DFB1FE3A40F7AC9B64C41D39360A7423828B97CB088A4903315E402A7089FA0F8B6C2355169CC9C99DFB44692A9B93DD",
        "y": "453ACA1243B5EC6B423A68A25587E1613A634C1C42D2EE7E6C57F449A1C91DC89168B7036EC0A7F37A366185233EC522",
    },
    {
        "k": "19",
        "x": "8D481DAB912BC8AB16858A211D750B77E07DBECCA86CD9B012390B430467AABF59C8651060801C0E9599E68713F5D41B",
        "y": "A1592FF0121460857BE99F2A60669050B2291B68A1039AA0594B32FD7ADC0E8C11FFBA5608004E646995B07E75E52245",
    },
    {
        "k": "20",
        "x": "605508EC02C534BCEEE9484C86086D2139849E2B11C1A9CA1E2808DEC2EAF161AC8A105D70D4F85C50599BE5800A623F",
        "y": "5158EE87962AC6B81F00A103B8543A07381B7639A3A65F1353AEF11B733106DDE92E99B78DE367B48E238C38DAD8EEDD",
    },
    {
        "k": "112233445566778899",
        "x": "A499EFE48839BC3ABCD1C5CEDBDD51904F9514DB44F4686DB918983B0C9DC3AEE05A88B72433E9515F91A329F5F4FA60",
        "y": "3B7CA28EF31F809C2F1BA24AAED847D0F8B406A4B8968542DE139DB5828CA410E615D1182E25B91B1131E230B727D36A",
    },
    {
        "k": "112233445566778899112233445566778899",
        "x": "90A0B1CAC601676B083F21E07BC7090A3390FE1B9C7F61D842D27FA315FB38D83667A11A71438773E483F2A114836B24",
        "y": "3197D3C6123F0D6CD65D5F0DE106FEF36656CB16DC7CD1A6817EB1D51510135A8F492F72665CFD1053F75ED03A7D04C9",
    },
    {
        "k": "10158184112867540819754776755819761756724522948540419979637868435924061464745859402573149498125806098880003248619520",
        "x": "F2A066BD332DC59BBC3D01DA1B124C687D8BB44611186422DE94C1DA4ECF150E664D353CCDB5CB2652685F8EB4D2CD49",
        "y": "D6ED0BF75FDD8E53D87765FA746835B673881D6D1907163A2C43990D75B454294F942EC571AD5AAE1806CAF2BB8E9A4A",
    },
    {
        "k": "9850501551105991028245052605056992139810094908912799254115847683881357749738726091734403950439157209401153690566655",
        "x": "5C7F9845D1C4AA44747F9137B6F9C39B36B26B8A62E8AF97290434D5F3B214F5A0131550ADB19058DC4C8780C4165C4A",
        "y": "712F7FCCC86F647E70DB8798228CB16344AF3D00B139B6F8502939C2A965AF0EB4E39E2E16AB8F597B8D5630A50C9D85",
    },
    {
        "k": "9850502723405747097317271194763310482462751455185699630571661657946308788426092983270628740691202018691293898608608",
        "x": "DD5838F7EC3B8ACF1BECFD746F8B668C577107E93548ED93ED0D254C112E76B10F053109EF8428BFCD50D38C4C030C57",
        "y": "33244F479CDAC34F160D9E4CE2D19D2FF0E3305B5BF0EEF29E91E9DE6E28F678C61B773AA7E3C03740E1A49D1AA2493C",
    },
    {
        "k": "1146189371817832990947611400450889406070215735255370280811736587845016396640969656447803207438173695115264",
        "x": "CB8ED893530BFBA04B4CA655923AAAD109A62BC8411D5925316C32D33602459C33057A1FBCB5F70AEB295D90F9165FBC",
        "y": "426AEE3E91B08420F9B357B66D5AFCBCF3956590BF5564DBF9086042EB880493D19DA39AAA6436C6B5FC66CE5596B43F",
    },
    {
        "k": "9619341438217097641865390297189708858938017986426152622639500179774624579127744608993294698873437325090751520764",
        "x": "67F714012B6B070182122DDD435CC1C2262A1AB88939BC6A2906CB2B4137C5E82B4582160F6403CAB887ACDF5786A268",
        "y": "90E31CF398CE2F8C5897C7380BF541075D1B4D3CB70547262B7095731252F181AC0597C66AF8311C7780DB39DEC0BD32",
    },
    {
        "k": "1231307996623833742387400352380172566077927415136813282735641918395585376659282194317590461518639141730493780722175",
        "x": "55A79DF7B53A99D31462C7E1A5ED5623970715BB1021098CB973A7520CBD6365E613E4B2467486FB37E86E01CEE09B8F",
        "y": "B95AEB71693189911661B709A886A1867F056A0EFE401EE11C06030E46F7A87731DA4575863178012208707DD666727C",
    },
    {
        "k": "587118838854683800942906722504810343086699021451906946003274128973058942197377013128840514404789143516741631",
        "x": "9539A968CF819A0E52E10EEA3BACA1B6480D7E4DF69BC07002C568569047110EE4FE72FCA423FDD5179D6E0E19C44844",
        "y": "A7728F37A0AE0DF2716061900D83A4DA149144129F89A214A8260464BAB609BB322E4E67DE5E4C4C6CB8D25983EC19B0",
    },
    {
        "k": "153914077530671739663795070876894766451466019374644150541452557147890542143280855693795882295846834387672681660416",
        "x": "933FC13276672AB360D909161CD02D830B1628935DF0D800C6ED602C59D575A86A8A97E3A2D697E3ED06BE741C0097D6",
        "y": "F35296BD7A6B4C6C025ED6D84338CCCC7522A45C5D4FBDB1442556CAEFB598128FA188793ADA510EB5F44E90A4E4BEF1",
    },
    {
        "k": "75148784606135150476268171850082176256856776750560539466196504390587921789283134009866871754361028131485122560",
        "x": "0CE31E1C4A937071E6EBACA026A93D783848BCC0C1585DAF639518125FCD1F1629D63041ABFB11FFC8F03FA8B6FCF6BF",
        "y": "A69EA55BE4BEAB2D5224050FEBFFBDFCFD614624C3B4F228909EB80012F003756D1C377E52F04FA539237F24DD080E2E",
    },
    {
        "k": "19691383761310193665095292424754807745686799029814707849273381514021788371252213000473497648851202400395528761229312",
        "x": "6842CFE3589AC268818291F31D44177A9168DCBC19F321ED66D81ECF59E31B54CCA0DDFD4C4136780171748D69A91C54",
        "y": "E3A5ECD5AC725F13DBC631F358C6E817EDCF3A613B83832741A9DB591A0BAE767FC714F70C2E7EA891E4312047DECCC0",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942623",
        "x": "605508EC02C534BCEEE9484C86086D2139849E2B11C1A9CA1E2808DEC2EAF161AC8A105D70D4F85C50599BE5800A623F",
        "y": "AEA7117869D53947E0FF5EFC47ABC5F8C7E489C65C59A0ECAC510EE48CCEF92116D16647721C984B71DC73C825271122",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942624",
        "x": "8D481DAB912BC8AB16858A211D750B77E07DBECCA86CD9B012390B430467AABF59C8651060801C0E9599E68713F5D41B",
        "y": "5EA6D00FEDEB9F7A841660D59F996FAF4DD6E4975EFC655FA6B4CD028523F172EE0045A8F7FFB19B966A4F828A1ADDBA",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942625",
        "x": "DFB1FE3A40F7AC9B64C41D39360A7423828B97CB088A4903315E402A7089FA0F8B6C2355169CC9C99DFB44692A9B93DD",
        "y": "BAC535EDBC4A1394BDC5975DAA781E9EC59CB3E3BD2D118193A80BB65E36E2366E9748FB913F580C85C99E7BDCC13ADD",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942626",
        "x": "4099952208B4889600A5EBBCB13E1A32692BEFB0733B41E6DCC614E42E5805F817012A991AF1F486CAF3A9ADD9FFCC03",
        "y": "A1306B8887CCFA67C6B8BA6B509FCA67E9C52C07FF752F32648682D880DC774BFB25B2CF55697F13059AF10B1DC4F65F",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942627",
        "x": "D5D89C3B5282369C5FBD88E2B231511A6B80DFF0E5152CF6A464FA9428A8583BAC8EBC773D157811A462B892401DAFCF",
        "y": "27EADD621ED6F92DBE7E92A1656BB70E2BE2B03BF1D5C42463545A81BBF585442EDEF3460B640DDC97DD48AB1454C98C",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942628",
        "x": "B3D13FC8B32B01058CC15C11D813525522A94156FFF01C205B21F9F7DA7C4E9CA849557A10B6383B4B88701A9606860B",
        "y": "EAD6E618206E9D59E4FB64DAC9E9B4E411453B5EE28B650B7B2EEEBC8C2040257C72DB064D7B50AF67A2A773CC08429D",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942629",
        "x": "E8C8F94D44FBC2396BBEAC481B89D2B0877B1DFFD23E7DC95DE541EB651CCA2C41ABA24DBC02DE6637209ACCF0F59EA0",
        "y": "76E51BBCA903751F6CD4340921AD3756CC479E6E188D728637CE6BEC5F62F0B603B9745EAAF621DD2811A362E4984777",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942630",
        "x": "A567BA97B67AEA5BAFDAF5002FFCC6AB9632BFF9F01F873F6267BCD1F0F11C139EE5F441ABD99F1BAAF1CA1E3B5CBCE7",
        "y": "21E4C74C6760CCE79BB1BEB850E9B133AE7AA6AFB96CD13F79CD641FA87A82988894347C8DDE75829BDC5ED9C90BD633",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942631",
        "x": "952A7A349BD49289AB3AC421DCF683D08C2ED5E41F6D0E21648AF2691A481406DA4A5E22DA817CB466DA2EA77D2A7022",
        "y": "5FCDF0507B4A43FA9CFAD215190990D1F6047FC931E75F1446FD74F69E694AF1FCE559B9768BC1DD610945341DE42E91",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942632",
        "x": "099056E27DA7B998DA1EEEC2904816C57FE935ED5837C37456C9FD14892D3F8C4749B66E3AFB81D626356F3B55B4DDD8",
        "y": "D1B3F3DCB1CF5469977AFAABB53A1FC6903B1127203C9C02BC006C0BE4AD5CD9AB992AEC9C5500CA82A2457FC73A1F44",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942633",
        "x": "A669C5563BD67EEC678D29D6EF4FDE864F372D90B79B9E88931D5C29291238CCED8E85AB507BF91AA9CB2D13186658FB",
        "y": "567748D5183ED860DD26F7C24A0F132208FEE6AAF3E7C3CE3AFD20873C48FA56D6927E69DB7D77266887B09648C5DE22",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942634",
        "x": "8F0A39A4049BCB3EF1BF29B8B025B78F2216F7291E6FD3BAC6CB1EE285FB6E21C388528BFEE2B9535C55E4461079118B",
        "y": "9D3881EBC749FE29BAD3B5ACDD3C56866564C2835C3BFF39489877AB51264CFC618BC100202AE497D9D25B075399B507",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942635",
        "x": "1692778EA596E0BE75114297A6FA383445BF227FBE58190A900C3C73256F11FB5A3258D6F403D5ECE6E9B269D822C87D",
        "y": "232DC9A8FF2BEF957CAC7745C24702F1DDAAB52392ADE32B42E3CF3D13F113E594521E15322E8F729095405CFDD4F52D",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942636",
        "x": "283C1D7365CE4788F29F8EBF234EDFFEAD6FE997FBEA5FFA2D58CC9DFA7B1C508B05526F55B9EBB2040F05B48FB6D0E1",
        "y": "6B8A366F9E1BE47745AD102473E96FB8E59E2798128668D62636D32FE242DDA8CF27B120CD5870619B99B3263AED1073",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942637",
        "x": "627BE1ACD064D2B2226FE0D26F2D15D3C33EBCBB7F0F5DA51CBD41F26257383021317D7202FF30E50937F0854E35C5DF",
        "y": "F68995B34C074E3DE41922593EB0EA8A4D36ACAD9BB088B36679B09EC8EABBE8FB3BA4717B1E9ACEE8CC5BF82C0F06CB",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942638",
        "x": "11DE24A2C251C777573CAC5EA025E467F208E51DBFF98FC54F6661CBE56583B037882F4A1CA297E60ABCDBC3836D84BC",
        "y": "705969388BBF06D2F0A7C816F5FF183AD7B4BB88AB2A211773679ACC496FE513CE889791F51704CCE7BBEB55193E8EC5",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942639",
        "x": "138251CD52AC9298C1C8AAD977321DEB97E709BD0B4CA0ACA55DC8AD51DCFC9D1589A1597E3A5120E1EFD631C63E1835",
        "y": "35351D679659D1E9CE175D7E7E54A99E923BA26E7543F60C54F19C3086D55B22128C7840C8445A96AB60E3FE4D8F1298",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942640",
        "x": "077A41D4606FFA1464793C7E5FDC7D98CB9D3910202DCD06BEA4F240D3566DA6B408BBAE5026580D02D7E5C70500C831",
        "y": "366A0835F4F3BD7C82F44169FD5603667ADF4BE37AEEA55A0897B3F123EEE1523DB542931B4A2D6749A0D7A0F5D0E20E",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942641",
        "x": "08D999057BA3D2D969260045C55B97F089025959A6F434D651D207D19FB96E9E4FE0E86EBE0E64F85B96A9C75295DF61",
        "y": "717F0E05A4E4C312484017200292458B4D8A278A43933BC16FB1AFA0DA954BD9A002BC15B2C61DD29EAFE190F56BF17F",
    },
    {
        "k": "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942642",
        "x": "AA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A385502F25DBF55296C3A545E3872760AB7",
        "y": "C9E821B569D9D390A26167406D6D23D6070BE242D765EB831625CEEC4A0F473EF59F4E30E2817E6285BCE2846F15F1A0",
    },
]

P384 = CurveParams()
P384.P = int(
    "39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319",
    10,
)
P384.N = int(
    "39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643",
    10,
)
P384.B = int(
    "b3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef",
    16,
)
P384.Gx = int(
    "aa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7",
    16,
)
P384.Gy = int(
    "3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f",
    16,
)
P384.BitSize = 384


@pytest.fixture
def p384():
    return P384


@pytest.mark.parametrize("p384_test_value", p384_test_data)
def test_p384_on_curve(p384, p384_test_value):
    assert p384.is_on_curve(
        int(p384_test_value["x"], 16), int(p384_test_value["y"], 16)
    )


@pytest.mark.parametrize("p384_test_value", p384_test_data)
def test_p384_scalar_mult(p384, p384_test_value):
    k_int = int(p384_test_value["k"], 10)
    k_bytes = k_int.to_bytes((k_int.bit_length() + 7) // 8, "big")
    gen_x, gen_y = p384.scalar_base_mult(k_bytes)
    assert gen_x == int(p384_test_value["x"], 16)
    assert gen_y == int(p384_test_value["y"], 16)


def test_p384_marshall(p384):
    priv, x, y = generate_key(p384)
    serialized = marshall(p384, x, y)
    xx, yy = unmarshall(p384, serialized)
    assert x == xx
    assert y == yy


def test_p384_overflow(p384):
    point_data = binascii.unhexlify(
        "049B535B45FB0A2072398A6831834624C7E32CCFD5A4B933BCEAF77F1DD945E08BBE5178F5EDF5E733388F196D2A631D2E075BB16CBFEEA15B"
    )
    x, y = unmarshall(p384, point_data)
    assert not p384.is_on_curve(x, y)
