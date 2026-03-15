# plaything_bot
- 심심해서 만든 Python Discord 봇.
- Built with Python, Discord.py
- 디코의 어느 한 서버에서만 작동함.

---
# 명령어

## 1. `!더해 num1 num2`

* **Param**

  * `num1 (int)` : 첫번째 수
  * `num2 (int)` : 두번째 수
* 첫번째 수하고 두번째 수를 더함

---

## 2. `!한판뜨자_애송이`

* **Param**

  * None
* 결투 신청임

---

## 3. `!가위바위보 user`

* **Param**

  * `user (가위 or 바위 or 보)` : 유저가 낼거
* 이겨보든가

---

## 4. `!소갈비찜_레시피`

* **Param**

  * None
* 가장 유용한 명령어임

---

## 5. `!랜덤 min max`

* **Param**

  * `min (int)` : 최솟값
  * `max (int)` : 최댓값
* min하고 max사이의 수를 뱉음

---

## 6. `!타이머 time`

* **Param**

  * `time (int, >0)` : 기다릴 초
* time초 만큼 기다림

---

## 7. `!유배_보내기 user`

* **Param**

  * `user (discord_user)` : 유배 보낼애
* user을 유배보냄. 롤 `"유배_관리인"`만 사용 가능

---

## 8. `!유배_풀어주기 user`

* **Param**

  * `user (discord_user)` : 유배 풀어줄 애
* user을 유배 풀어줌. 롤 `"유배_관리인"`만 사용 가능

---

## 9. `!유배_리스트`

* **Param**

  * None
* 유배당한 불쌍한 놈들을 리스트업 해줌

---

## 10. `!말해 text`

* **Param**

  * `text (str)` : 말할 텍스트
* 간지나게 디코방에 들어와서 text를 알맞은 언어에 맞게 읽어줌

---

## 11. `!뮤트 user`

* **Param**

  * `user (discord_user)` : 뮤트 할 애
* user을 뮤트 시킴

---

## 12. `!언뮤트 user`

* **Param**

  * `user (discord_user)` : 뮤트 풀 애
* user을 언뮤트 시킴

---

## 13. `!얼마있음 user`

* **Param**

  * `user (discord_user)` : 얼마있는지 궁금한 애
* user이 얼마가진지 확인

---

## 14. `!퀴즈`

* **Param**

  * None
* 퀴즈를 냄. Reply로 정답 제출 가능하고 맞추면 1000원임 ㅅㄱ

---

## 15. `!재생해 url loop`

* **Param**

  * `url (url)` : 재생할 유튜브 url
  * `loop (bool?)` : 반복재생 여부. True or False임. 기본은 False.
* url주면 유튜브에서 틀어줌

---

## 16. `!도박 money`

* **Param**

  * `money (int)` : 도박 할 돈. 자연수이며 니가 가진 돈 보단 작아야함
* money만큼의 돈 걸어서 지면 다 잃고 이기면 (건돈 * 배율)만큼 돈 범

---

## 17. `!돈줘`

* **Param**

  * None
* 하루마다 10000원 줌

---

## 18. `!급식`

* **Param**

  * None
* 오늘의 급식 받을 수 있음

---

## 19. !마크
* *Param*

   * act: AcrEnum(켜, 꺼, 상태)
* 마크 서버를 키거나 끄거나 상태 확인함
       
---


### ❗ 기타

그외 영어로 된거나 여기 없는 명령어들은 개발용임 ㅅㄱ

