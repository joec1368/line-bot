# Smile Bot:
- F74091093陳宥橋
![](https://i.imgur.com/iUTvnrR.png)


## 前言
最一開始的目的就只是單純的可以追蹤自家冰箱裡面有什麼。但在製作之於，想說就把它做成一個好用的小幫手！可以讓大家的日常生活，因為有了它，所以充滿著笑容！

## 構想
在最一開始的時候，有許多 Mode ，可以讓大家選擇要進去哪個模式使用。以下稍微介紹每個模式在做什麼：
* map : 
    * 可以在裡面選擇地點，然後藉由 一些package ，可以幫你抓到當地的位置，然後如果有特殊的物件，還可以爬照片給你！
* refrigerator : 
    * 在裡面，可以看到現在冰箱有什麼東西，以及新增和刪除
* playground : 
    * 在裡面，可以玩猜數字遊戲
* weather : 
    * 會藉由中央氣象局的資料，可以獲得 48 hr 內的氣象資料（舒適度、最高溫、最低溫等）
* news :
    * 會幫你在 bbc 上面爬最多人看的 top 5 新聞
     
## 環境 : 
* 部署 ： 選擇 dokcker python 3.8 的 image ，然後在render 上部署
* 資料庫 ： render 平台上的 postgresql

## 技術
* 在 map mode 裡面：
    * line api : 
        * LocationMessage ，可獲得 user 的地址資訊
        * ImageSendMessage : 用來傳輸照片
    * geopy : 用來抓取地址相關訊息
    * beautifulsoup : 用來抓取圖片相關訊息
* 在 refrigerator:
    * postgresql 
* 在 weather :
    * 中央氣象局的 api
* 在 news : 
    * beautifulsoup : 用來抓取新聞相關資訓
* 部署：
    * docker

## 使用教學
* init state，可以使用 help 去獲得相關資訊
    * ![](https://i.imgur.com/FT4VmTS.png)
* playground : 
    * 輸入 play ，可以進到 playground ，去玩猜數字的遊戲
        * ![](https://i.imgur.com/a3d7MrQ.png)
    * 輸入 guess number ( 1 ~ 100 )
        * ![](https://i.imgur.com/iObIAKE.png)
        * 會像圖片顯示一樣，會顯示數字要大一點或小一點
        * 當猜對後，會自動幫你換數字
* Map : 
    * 輸入 map 以後，會進入 map state，一進去會有提示訊息，告訴你如何使用
    * 然後可以利用手機上的地址功能，他便會告訴你他的位置資訊
    * ![](https://i.imgur.com/8pUksHD.jpg)
    * 如果該地址有特殊的東西，則可以使用 positionInfo 功能，他會幫你在網路上找圖，然後傳給你
    * ![](https://i.imgur.com/4E7yOye.jpg)
* News : 
    * 輸入 news : 可以進到 news state，一進去就會印出新聞資訊，也可以再次輸入 news ，來再次獲取資訊
    * ![](https://i.imgur.com/dY3IloW.png)
* Weather : 
    * 輸入 weather ，會進入 weather state，可以獲得 weather 相關資訊
    * 一進去，會請你輸入想要的地區，然後會告知你可以獲得的資訊
    * ![](https://i.imgur.com/4mAHXLm.png)
    * 以下展示可以貨的得資訊：
        * weather info
            * ![](https://i.imgur.com/YdVSj3U.png)
        * highest temperature
            * ![](https://i.imgur.com/CDjebwg.png)
        * lowest temperature
            * ![](https://i.imgur.com/bgsBmDK.png)
        * comfort info
            * ![](https://i.imgur.com/kzuL6zs.png)
        * property of rain
            * ![](https://i.imgur.com/pcv4Zj0.png)
* refrigetor : 
    * 輸入 refrigerator，可以進入 refrigetor state，一進去會顯示相關資訊
    * ![](https://i.imgur.com/48nCzSJ.png)
    * 輸入 help，查看可以使用的 command
    * ![](https://i.imgur.com/4mvPisI.png)
    * 輸入 db，看現在冰箱裡有什麼
        * 會告知名稱，和哪時候過期
    * ![](https://i.imgur.com/8TxetKh.png)
    * 輸入 new ，添加新東西進冰箱
    * ![](https://i.imgur.com/J4vuT2m.png)
    * 輸入 delete ，刪除吃玩的東西
    * ![](https://i.imgur.com/XuwTnvO.png)
* 輸入 exit ，就可以回到最一開始的 state

## FSM
![](https://i.imgur.com/bzCFwor.png)

## Deploy in Render
利用 dockerfile， render 會利用這個 dockerfile ，幫你建成docker image，並把他部署上去


