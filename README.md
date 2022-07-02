## 功能預覽
* Twitter (3s / per account)
![image](https://cdn.discordapp.com/attachments/975334386935427122/992833846120808700/unknown.png)
* Youtube (11s / per account)
![image](https://cdn.discordapp.com/attachments/975334386935427122/992834005256912997/unknown.png)
* YoutubeLive (15m / per account)
尚無，待更新
* Vlive (5m / per account)
    - 新影片
    ![image](https://cdn.discordapp.com/attachments/975334386935427122/992834352373321869/unknown.png)
    - 新直播
    ![image](https://cdn.discordapp.com/attachments/975334386935427122/992834506585276556/unknown.png)
    - 新貼文
    尚無，待更新
* Instagram (5m / per account)
    - 新貼文
    ![image](https://cdn.discordapp.com/attachments/975334386935427122/992834787159060511/unknown.png)
    - 新限時動態
    ![image](https://cdn.discordapp.com/attachments/975334386935427122/992835006646988950/unknown.png)

## 前置作業  
* requirements.txt的py套件請安裝，可能不完全，若執行時有缺少請順便安裝後回報

因為礙於個資跟api的限制，所以檔案下載之後請在**secretdata.json**處打上以下資料  
* Discord bot Token
* Twitter API key & guestId (在postman上的示範code中取得)
* Youtube API key 兩個 (一般影片通知 & Live通知)
* Instagram 帳號密碼 (建議使用備用的，太頻繁登入有可能會被鎖)

## 指令
### 追蹤帳號註冊 (以下連結皆可複數以上)
* Twitter
    - twiadd [帳號連結]
* Youtube
    - ytadd_id [頻道連結] ***注意並不接受https://www.youtube.com/c/[帳號名稱]**
    - ytadd_vid [影片連結]
* YoutubeLive
    - ytlivadd_id [頻道連結] ***注意並不接受https://www.youtube.com/c/[帳號名稱]**
    - ytlivadd)vid [影片連結]
* Vlive
    - vliadd [頻道連結]
* Instagram
    - login ***使用此功能之前皆須要先執行此指令，不然在註冊以及開始追蹤時會失敗**
    - insadd [帳號連結]
* 選擇發布頻道
    - 在以上指令執行完後會跳出通知要您選擇發布的頻道，**請使用頻道的ID**

### 資料搜尋 / 刪除 / 修改
* 資料搜尋
    - datafol [twi / yt / ytl / vli / ins]
* 資料刪除
    - datadel [twi / yt / ytl / vli / ins] [想要刪除的帳號id]
* 資料修改
    - dataset [twi / yt / ytl / vli / ins] [想要修改的帳號的發布頻道] 

### 開始執行追蹤
* [twi / yt / ytl / vli / ins] + _update_start
* [twi / yt / ytl / vli / ins] + _update_stop

### 一些注意事項
* 開始執行追蹤時是每間隔一段時間換下一個帳號更新，所以**新增的帳號越多，每一個帳號到下一次被輪到的時間會越長**
* 想要縮短間格時間可直接至Taskloop.py更改，更改完後請重新開啟機器人，**Youtube和YoutubeLive的部分已經設成最小值，再小會有扣打爆掉的問題(見事項4)，Vlive和Instagram的部分若縮太小會有執行不完全以及被官方判定為爬蟲程式鎖IP的可能，後果自負**
* Twitter的API限制是每十五分鐘可以call 900次，故使用者每三秒不宜使用新增指令超過兩次，**建議在新增時一次就新增完成**
* Youtube的API每日有10000的扣打，每使用一次新增指令/查找一個帳號一次將會消耗一次扣打，Live的部分每查找一個帳號一次就是消耗一百扣打，所以**兩個API需要分開，API共用會有扣打爆炸的問題**
* Vlive的部分因為無法追蹤時間，所以使用最後一支影片ID/文章ID作為判斷，**若途中該支影片被刪除將無法判斷，將會往後抓三支影片作為更新發布**
* Vlive和Instagram的新增指令因為是使用爬蟲的方式完成，所以速度執行上會較慢，請耐心等候，若等待時間過長(超過一分鐘)，請到監控畫面查看問題並回報
* Instagram的部分因為資料是用爬蟲的方式完成，所以在**執行新增指令以及執行追蹤的時間請盡量避開**，建議是先新增完成再選擇執行，若執行途中想要新增建議先暫停，等新增完成之後再繼續執行
* 如果看得懂我很醜的code也可以自己改