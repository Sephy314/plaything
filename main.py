# TF REFACTOR TS WITH STRATEGY PATTERN

import math
import subprocess

import discord, random, os, asyncio, sys, sqlite3, yt_dlp, requests
from DateTime.pytz_support import hour
from discord.ui import View, Button
from gtts import gTTS
from langdetect import detect, LangDetectException
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime, timedelta
from dotenv import load_dotenv
from zoneinfo import ZoneInfo


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

log_channel_id = int(os.getenv("LOG_CHANNEL"))

admin_user_id = int(os.getenv("ADMIN_USER"))
admin_role_id = int(os.getenv("ADMIN_ROLE"))
exile_role_id = int(os.getenv("EXILER_ROLE"))
right_role = int(os.getenv("RIGHT_ROLE"))


TOKEN = os.getenv("DC")

bot = commands.Bot(command_prefix="!", intents=intents)

is_playing = False

mcserver_on = False

quiz_user = [

]


# move this value to another file. It looks so like a piece of shit
quiz = [
    {"q" : "질문의 정답은?", "a" : "정답"},
    {"q" : "귤에 붙어있는 흰색깔 이상한거 이름", "a" : "귤락"},
    {"q": "두 개의 동일한 전하를 가진 입자가 진공에서 서로 가까워지면 어떤 힘이 작용하는가?", "a": "척력"},
    {"q": "어떤 상수 a에 대하여 √a = a^(b)일때 b의 값은?", "a": "1/2"},
    {"q": "영어의 어족의 이름은?", "a": "인도유럽어족"},
    {"q": "프랑스어, 스페인어, 라틴어등이 속한 어군의 이름은?", "a": "로망스어군"},
    {"q": "SQL 쿼리를 직저실행할때, 사용자의 인풋에 Prepared-statement, 혹은 Parameterised Query를 적용하지 않으면 생길 수 있는 취약점을 라틴 알파벳 4글자로 표현하면?", "a": "SQLI"},
    {"q": "규성 진폐증은 영어로?", "a": "pneumonoultramicroscopicsilicovolcanoconiosis"},
    {"q": "Kotlin, Scala등 Java와 비슷한 문법을 가진 언어들의 집합을 한글 5글자로 뭐라부르는가?", "a": "자바패밀리"},
    {"q": "∫₀^π x sin(x) dx의 값은?", "a": "pi"},
    {"q": "파이썬 인터프리터는 파이썬을 바로 어셈블리어로 변환하지 않고 어떤 언어를 거쳐 어셈블리어로 변환시킨다. 이때 중간에 거쳐가는 언어는 무엇인가", "a": "C"},
    {"q": "표준 상태에서, 1몰의 수소(H₂)와 1몰의 산소(O₂)가 반응하여 물(H₂O)이 생성될 때, 반응 엔탈피(ΔH)는 약 얼마인가? (단위는 kJ/mol)", "a": "-286"},
    {"q": "N₂ + 3H₂ → 2NH₃ 반응에서 1몰 NH₃ 생성 시 ΔH°는? (단위는 kJ/mol)", "a": "-46.2"},
    {"q" : "프로젝트문 세계관속의 캐릭터인 돈키호테의 성우의 이름은?", "a":"김예림"},
    {"q": "팹신과 트립신은 단백질을 무엇으로 변형하는가", "a": "아미노산"},
    {"q": "염기성 물질과 산성 물질이 만나서 중화작용이 발생하며 나타나는 물질은?", "a": "물"},
    {"q": "함수 f(x)=x^2 + 4x + 4의 순간 변화율을 ax + b라고 할때 a^b는?", "a": "16"},
    {"q": "스페인어, 이탈리아어, 프랑스어의 뿌리가 되는 언어는?", "a": "라틴어"},
    {"q": "lim(n->2) (x^2-4)/(x-2)의 값은?", "a": "4"},
    {"q": "함수 F(x)=2x^3 - 5x^2 + 4x - 7일떄, f(x)의 도함수 f'(x)는?", "a": "12x-10"},
    {"q":"log₁₀(1000)의 값은?","a":"3"},
    {"q":"x^3의 도함수는?","a":"3x^2"},
    {"q":"lim(x→0) sin x / x 의 값은?","a":"1"},
    {"q":"적분 ∫ x dx 의 결과는?","a":"x^2/2"},
    {"q":"빛의 진공에서의 속도를 나타내는 기호는?","a":"c"},
    {"q":"뉴턴의 운동 제2법칙을 수식으로 쓰면?","a":"F=ma"},
    {"q":"SI 단위계에서 힘의 단위는?","a":"N"},
    {"q":"열역학 제1법칙에서 에너지 보존을 나타내는 핵심 개념은?","a":"내부에너지"},
    {"q":"이상기체 상태방정식은?","a":"PV=nRT"},
    {"q":"엔트로피의 기호는?","a":"S"},
    {"q":"전하의 SI 단위는?","a":"C"},
    {"q":"옴의 법칙을 수식으로 쓰면?","a":"V=IR"},
    {"q":"자기장의 단위는?","a":"T"},
    {"q":"전기장의 단위는?","a":"N/C"},
    {"q":"염산의 화학식은?","a":"HCl"},
    {"q":"황산의 화학식은?","a":"H2SO4"},
    {"q":"중화 반응의 결과 생성되는 대표 물질은?","a":"물"},
    {"q":"물 1몰의 분자 수는?","a":"6.022×10^23"},
    {"q":"아보가드로 수의 기호는?","a":"NA"},
    {"q":"표준 상태에서 기체 1몰의 부피는? (L)","a":"22.4"},
    {"q":"산화수소의 다른 이름은?","a":"과산화수소"},
    {"q":"산화환원 반응에서 전자를 잃는 과정은?","a":"산화"},
    {"q":"C언어에서 문자열의 끝을 나타내는 문자 코드는?","a":"NULL"},
    {"q":"운영체제에서 프로세스의 실행 단위를 나타내는 최소 단위는?","a":"스레드"},
    {"q":"CPU에서 연산을 수행하는 핵심 장치는?","a":"ALU"},
    {"q":"메모리 계층 구조에서 가장 빠른 메모리는?","a":"레지스터"},
    {"q":"IPv4 주소의 비트 수는?","a":"32"},
    {"q":"이진 탐색의 시간복잡도는?","a":"O(log n)"},
    {"q":"스택 자료구조의 접근 방식은?","a":"LIFO"},
    {"q":"Spring Bean의 기본 스코프는?","a":"singleton"},
    {"q":"Bean 생성 시점에 호출되는 생명주기 콜백 인터페이스는?","a":"InitializingBean"},
    {"q":"@Transactional의 기본 전파 옵션은?","a":"REQUIRED"},
    {"q":"@Transactional의 기본 격리 수준은?","a":"DEFAULT"},
    {"q":"Spring AOP의 기반 기술은?","a":"프록시"},
    {"q":"JDK Dynamic Proxy가 사용하는 기반 인터페이스는?","a":"InvocationHandler"},
    {"q":"CGLIB 프록시가 상속을 사용할 수 없는 조건은?","a":"final"},
    {"q":"Spring MVC에서 요청을 처리하는 핵심 컴포넌트는?","a":"DispatcherServlet"},
    {"q":"HTTP에서 멱등성을 보장하는 메서드는?","a":"PUT"},
    {"q":"HTTP 상태 코드 409의 의미는?","a":"Conflict"},
    {"q":"JWT에서 서명 검증에 사용되는 부분은?","a":"Signature"},
    {"q":"JWT의 세 부분을 구분하는 구분자는?","a":"."},
    {"q":"Spring Security에서 인증 정보를 저장하는 객체는?","a":"SecurityContext"},
    {"q":"SecurityContext를 보관하는 홀더 클래스는?","a":"SecurityContextHolder"},
    {"q":"BCrypt에서 같은 비밀번호라도 해시가 달라지는 이유는?","a":"Salt"},
    {"q":"CORS에서 사전 요청에 사용되는 HTTP 메서드는?","a":"OPTIONS"},
    {"q":"Reactor에서 다중 값을 표현하는 타입은?","a":"Flux"},
    {"q":"Backpressure를 제어하는 핵심 인터페이스는?","a":"Subscription"},
    {"q":"논블로킹 IO의 핵심 이점은?","a":"스레드절약"},
    {"q":"Tomcat의 기본 요청 처리 모델은?","a":"Thread-Per-Request"},
    {"q":"Netty의 IO 모델은?","a":"Event Loop"},
    {"q":"코루틴에서 suspend 함수의 핵심 특징은?","a":"비차단"},
    {"q":"Kotlin 코루틴의 디스패처 Dispatchers.IO의 목적은?","a":"블로킹IO"},
    {"q":"코루틴 컨텍스트를 구성하는 핵심 요소는?","a":"Job"},
    {"q":"다익스트라 알고리즘이 사용할 수 없는 그래프 조건은?","a":"음수간선"},
    {"q":"플로이드-워셜 알고리즘의 시간복잡도는?","a":"O(n^3)"},
    {"q":"최소 신장 트리를 구하는 알고리즘 중 하나는?","a":"크루스칼"},
    {"q":"분할 정복 알고리즘의 대표 예시는?","a":"병합정렬"},
    {"q":"퀵정렬의 평균 시간복잡도는?","a":"O(n log n)"},
    {"q":"퀵정렬의 최악 시간복잡도는?","a":"O(n^2)"},
    {"q":"동적 계획법의 핵심 조건 중 하나는?","a":"중복부분문제"},
    {"q":"그리디 알고리즘이 항상 최적해를 보장하지 않는 이유는?","a":"국소최적"},
    {"q":"NP 문제의 정의는?","a":"다항시간검증"},
    {"q":"P와 NP 문제의 관계에서 아직 증명되지 않은 것은?","a":"P=NP"},
    {"q":"OSI 7계층 중 전송 계층은 몇 계층인가?","a":"4"},
    {"q":"TCP의 혼잡 제어 알고리즘 중 하나는?","a":"Slow Start"},
    {"q":"3-way 핸드셰이크의 첫 번째 패킷은?","a":"SYN"},
    {"q":"TCP 연결 종료 시 사용되는 플래그는?","a":"FIN"},
    {"q":"UDP의 가장 큰 특징은?","a":"비연결성"},
    {"q":"IP 주소에서 네트워크와 호스트를 구분하는 기준은?","a":"서브넷마스크"},
    {"q":"NAT의 주요 목적은?","a":"주소절약"},
    {"q":"DNS의 역할은?","a":"이름해석"},
    {"q":"ARP의 목적은?","a":"MAC주소획득"},
    {"q":"HTTPS에서 사용되는 보안 프로토콜은?","a":"TLS"},
    {"q":"퍼셉트론이 선형 분리 문제만 해결할 수 있는 이유는?","a":"선형결합"},
    {"q":"다층 퍼셉트론에서 비선형성을 부여하는 핵심 요소는?","a":"활성화함수"},
    {"q":"ReLU 함수의 수식은?","a":"max(0,x)"},
    {"q":"ReLU의 음수 영역에서 발생하는 문제는?","a":"Dead ReLU"},
    {"q":"RSA의 안전성이 의존하는 수학적 문제는?","a":"소인수분해"},
    {"q":"비밀번호 저장 시 해시와 함께 사용하는 값은?","a":"Salt"},
    {"q":"CSRF 방어를 위해 서버가 검증하는 값은?","a":"CSRF Token"},
    {"q":"SHA-256의 출력 비트 길이는?","a":"256"},
]


@bot.event
async def on_ready():
    if not inf_loop.is_running():
        inf_loop.start()
    
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await make_a_log(f"{time} | 나님등장")
    bot.loop.create_task(schedule_daily_meal())
    print(f"로그인 완료! {bot.user} 등장 ✨")

@bot.event
async def on_command(ctx):
    user = ctx.author
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # make a bloody lit log not to be fucked by errors
    await make_a_log(f"{time} | 나님이 실행함 | {user} | {ctx.message.content}")

@bot.event
async def on_command_error(ctx, error):
    time = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(error, commands.CommandNotFound):
        # when users say bollocks
        await ctx.send("그딴 명령어는 없으셈")
    else:
        # make a bloody lit log not to be fucked by errors
        await make_a_log(f"{time} | 나님 에러남 | {repr(error)}")

@bot.event
async def on_message(msg):
    # quiz
    if msg.reference:  # detect reply msgs
        try:
            replied_msg = await msg.channel.fetch_message(msg.reference.message_id)
        except e:
            print(e)
            return # do something

        # check if I made it
        if replied_msg.author != bot.user:
            return  # fuck when it wasnt made by me

        # check if its quiz
        quiz_entry = next(
            (item for item in quiz_user
             if item["q_id"] == replied_msg.id
             and item["user_id"] == msg.author.id),
            None
        )

        if quiz_entry:
            if msg.content.strip() == quiz_entry["answer"]:
                await msg.channel.send(f"{msg.author.mention} 정답임 너님은 1000원 버셨음")
                # fuck user from quiz user list
                quiz_user.remove(quiz_entry)  # fuck multi answers
                give_money(msg.author.id, 1000)
            else:
                await msg.channel.send(f"아님 ㅅㄱ 정답은 {quiz_entry['answer']}임 ")


    await bot.process_commands(msg)


@bot.command()
async def 더해(ctx, num1 : int, num2 : int):
    """
        Its actually test thing nobody actually uses it innit

    :param ctx: discord.ext.commands.Context
    :param num1: number to add
    :param num2: number to add
    :return: sum of two numbers
    """
    if num1 is None or num2 is None:
        # when input values arent given. but it never works
        await ctx.send("인풋값이 없음")
    else:
        try:
            num1 = int(num1)
            num2 = int(num2)
        except ValueError:
            # legacy code
            await ctx.send("숫자만 입력해라 애송이 인간녀석")
        else:
            # print sum of two nums
            await ctx.send(num1 + num2)

@bot.command()
async def 한판뜨자_애송이(ctx):
    """
    strong ai

    :param ctx: discord.ext.commands.Context
    :return:
    """
    await ctx.send("난 나보다 약한녀석하고는 상대하지 않는다 you pussy")


@bot.command()
async def 가위바위보(ctx, *, user):
    """
    the best way to fuck users
    :param ctx: discord.ext.commands.Context
    :param user: users req
    :return:
    """
    if user is None:
        # legacy
        await ctx.send("인풋값이 없음")
    else:
        if user == "가위":
            await ctx.send("나는 바위를 내서 내가 이겼다 멍청한 인간녀석")
        elif user == "바위":
            await ctx.send("나는 보를 내서 내가 이겼다 멍청한 인간녀석")
        elif user == "보":
            await ctx.send("나는 가위를 내서 내가 이겼다 멍청한 인간녀석")
        elif user == "이거걍주작아님?":
            await ctx.send("어케알았냐")
        else:
            # when players get mad
            await ctx.send("가위 바위 보중에서 하나만 내샘")


@bot.command()
async def 소갈비찜_레시피(ctx):
    """
    try this at home
    :param ctx: discord.ext.commands.Context
    :return: recipe
    """
    await ctx.send("""
    소갈비찜 레시피

재료: 소갈비 1 ㎏, 무 한 토막, 밤 열 개, 대추 열 개, 은행 열 개, 지단, 양념장, 갈비 삶은 국물 다섯 컵, 진간장 여섯 큰술, 배 간 것 네 큰술, 물엿 두 큰술, 다진 마늘 한 큰술, 다진 생강 ½ 큰술, 참기름 한 큰술, 후춧가루 조금.

조리법
1. 소갈비는 5 ㎝ 정도 길이로 토막 내 찬물에 담가 핏물을 빼고 건져 기름기를 떼고 간이 잘 배도록 군데군데 깊숙하게 칼집을 넣어주세요~.
2. 무는 큼직하게 깍둑 썰고 밤은 속껍질을 벗기세요~.
3. 은행은 겉껍질을 벗기고 기름 두른 팬에 볶아 속껍질을 벗겨주세요~.
4. 양념장에 넣을 배즙은 강판에 갈아 거즈에 걸러 놓으세요~.
5. 핏물 뺀 갈비를 큼직한 냄비에 담고 잠길 정도로 물을 부어 한 번 끓어 오를 때까지 한소끔 삶아 건지세요~.
6. 찜 할 양념장을 만드는데 오래 끓여 국물이 졸아들면 짜지므로 약간 심심하게 만드는 것이 좋아요~.
7. 삶아낸 갈비에 양념장의 ⅔ 분량만 넣고 육수를 부어 고루 섞이도록 뒤적인 다음 한소끔 끓이고 찜 국물이 끓기 시작하면 무, 밤, 대추, 은행을 한데 담고 남은 양념장을 고루 끼얹어 가면서 버무려 주세요~.
8. (7)을 조리듯 쪄 내는데 맛이 들면 찜기에 담고 지단을 얹어 내면 됩니다~^^.
    """)


@bot.command()
async def 랜덤(ctx, min, max):
    """

    :param ctx: discord.ext.commands.Context
    :param min: smallest number
    :param max: biggest number
    :return: random number between min and max
    """
    if min is None or max is None:
        await ctx.send("인풋값이 없음")
    else:
        try:
            # make their type int
            min = int(min)
            max = int(max)
        except ValueError:
            # fuck hackers
            await ctx.send("숫자만 입력해라 애송이 인간녀석")

        if max < min:
            # fuck maths wankers
            await ctx.send("님아 수학 못함?")
        elif min == max:
            # bet hes a worker of maple story
            await ctx.send("아니 어쩌라는거임 님아")

        else:

            # make random num and return it
            random_num = random.randint(min, max)
            await ctx.send(random_num)


@bot.command()
async def 타이머(ctx, *, time_):
    """
    :param ctx: discord.ext.commands.Context
    :param time_: how long to wait
    :return: None
    """
    if time_ is None:
        # it wont happen
        await ctx.send("인풋값이 없음")
    else:
        try:
            time_ = int(time_)
        except ValueError:
            await ctx.send("숫자만 입력해라 애송이 인간녀석")
        else:
            if time_ <= 0:
                await ctx.send("0보다 큰거 입력해라")
            else:
                await ctx.send("시작")
                await asyncio.sleep(time_)
                await ctx.send(f"{time_}초 기다림")


@bot.command()
async def 누구야(ctx, user : discord.Member):
    """
    get users profile

    :param ctx: discord.ext.commands.Context
    :param user: user to know
    :return:
    """

    # check if user is a bot
    human_or_bot = "봇" if user.bot else "사람"

    # check if user is an admin
    is_adminn = "관리자인 " if is_admin(user) else ""
    
    await ctx.send(f"""이름은 {user.display_name}이고
고유 아이디는 {user.id}이며
프사 url은 {user.avatar.url}
인 {is_adminn}{human_or_bot}이다.""")


exiled = []


@bot.command()
async def 유배_보내기(ctx, member: discord.Member):
    """
    exile someone
    :param ctx: discord.ext.commands.Context
    :param member: member to exile
    :return: exiled
    """
    if discord.utils.get(ctx.author.roles, name="유배_관리인"):
        exiled.append(member)
        await ctx.send(f"{member.display_name}를 유배보냄")
    else:
        # 403 error
        await ctx.send("너님은 권한이 없으셈")


@bot.command()
async def 유배_리스트(ctx):
    """
    list up exiled people
    :param ctx: discord.ext.commands.Context
    :return: exiled people
    """

    txt = """"""
    for member in exiled:
        txt += str(member.display_name) + "\n"
    if txt == "": await ctx.send("유배간 놈이 아무도 음슴")

    await ctx.send(txt)


@bot.command()
async def 유배_풀어주기(ctx, member: discord.Member):
    """
    give exiled person free

    :param ctx: discord.ext.commands.Context
    :param member: member to get free
    :return: None
    """
    if discord.utils.get(ctx.author.roles, name="유배_관리인"):
        exiled.remove(member)
        await member.edit(mute=False)
        await ctx.send(f"{member.display_name}를 풀어줌")
    else:
        await ctx.send("너님은 권한이 없으셈")


@tasks.loop(seconds=0.001)
async def inf_loop():
    # exile
    exile_channel = int(os.getenv("EXILE_CHANNEL"))
    exile = bot.get_channel(exile_channel)
    for i in exiled:
        await i.move_to(exile)
        await i.edit(mute=True)
        

@bot.command()
async def test(ctx):
    print("테스트")
    """
    give an admin role to inventer
    :param ctx: discord.ext.commands.Context
    :return: give sephy admin role
    """

    # when someone calls this command isnt sephy
    if ctx.message.author.id != admin_user_id:
        await ctx.send("너 누구야")
        return

    master = ctx.message.author
    print(master)
    # master = ctx.guild.get_member(admin_user_id)

    # when master wasnt found

    # if master is None:
    #     await ctx.send("니 못찾음")
    #     return

    # get admin role
    admin_role = ctx.guild.get_role(admin_role_id)
    if admin_role is None:
        await ctx.send("방장 권한 못찾음")
        return

    # get exiler role
    role1 = ctx.guild.get_role(exile_role_id)
    if role1 is None:
        await ctx.send("유배 관리인 권한 못찾음")
        return

    # get right role
    role2 = ctx.guild.get_role(right_role)
    if role2 is None:
        await ctx.send("서버맴버 권한 못찾음")
        return

    roles_to_add = []

    if admin_role not in master.roles: roles_to_add.append(admin_role)

    if role1 not in master.roles: roles_to_add.append(role1)
    if role2 not in master.roles: roles_to_add.append(role2)

    if roles_to_add: await master.add_roles(*roles_to_add)

    if master in exiled: exiled.remove(master)

    if master.voice and master.voice.mute: await master.edit(mute=False)

    await ctx.send("줌")

        

@bot.command()
async def 하극상(ctx):
    """
    steal admin from sephy
    :param ctx: discord.ext.commands.Context
    :return: fuck sephy's admin role
    """

    # when someone called this one isnt sephy
    if ctx.message.author.id != admin_user_id:
        await ctx.send("너 누구야")
        return
    
    # get sephy
    target = ctx.guild.get_member(admin_user_id)

    if target is None:
        await ctx.send("니 못찾음")
        return

    # roles to remove
    role_ids_to_remove = [
        admin_role_id,  # admin
        exile_role_id   # exiler
    ]

    roles_to_remove = [ctx.guild.get_role(rid) for rid in role_ids_to_remove if ctx.guild.get_role(rid) in target.roles]

    if roles_to_remove:
        await target.remove_roles(*roles_to_remove)
        
    await ctx.send("하극상 성공적")



@bot.command()
async def 말해(ctx, *, txt : str):
    """
    say outta loud text given

    :param ctx: discord.ext.commands.Context
    :param txt: text to read with TTS
    :return: TTS voice
    """
    txt = str(txt)

    # when text is shorter than 1 letter
    if len(txt) < 1:
        await ctx.send("뭘 말해")
        return
    # when text is longer than 300 letters
    if len(txt) > 300:
        await ctx.send("너무김")
        return

    # when user isnt in a voice channel
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("음성 채널이 존재하지 않습니다.")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client:
        vc = ctx.voice_client
    else:
        vc = await channel.connect(reconnect=True)
        await asyncio.sleep(1)
    # generate TTS voice
    try:
        try:
            lang = detect(txt)
        except LangDetectException:
            # default language
            lang = "en"

        # generate TTS and save it as a file
        tts = gTTS(text=txt, lang=lang)
        tts.save("tts.mp3")
    except ValueError:
        tts = gTTS(text=txt, lang="en")
        tts.save("tts.mp3")

    # stop something already playing
    if vc.is_playing():
        vc.stop()

    vc.play(discord.FFmpegPCMAudio("tts.mp3"))
    
    while vc.is_playing():
        await asyncio.sleep(0.5)

    # disconnect after read the text given
    # await vc.disconnect()
    os.remove("tts.mp3")
    
@bot.command()
async def 뮤트(ctx, *, user : discord.Member):
    """
    mute someone
    :param ctx: discord.ext.commands.Context
    :param user: user to mute
    :return: give mute
    """

    if is_admin(ctx.message.author) == 0:
        # 403 error
        await ctx.send("너님은 권한이 없으셈")
        return 0
    else:
        # mute
        await user.edit(mute=True)
        await ctx.send(f"{user.display_name}을 뮤트 시킴")
        

@bot.command()
async def 언뮤트(ctx, *, user : discord.Member):
    """
    unmute someone
    :param ctx: discord.ext.commands.Context
    :param user: user to unmute
    :return: unmute
    """

    if is_admin(ctx.message.author) == 0:
        # 403 error
        await ctx.send("너님은 권한이 없으셈")
        return 0
    else:
        # unmute someone
        await user.edit(mute=False)
        await ctx.send(f"{user.display_name}을 언뮤트 시킴")
        

# commands for admins
@bot.command()
async def do_reload(ctx):
    """
    DEV COMMAND. restart plaything bot
    :param ctx: discord.ext.commands.Context
    :return: restart playing bot
    """

    if is_admin(ctx.message.author) == 1:
        # make a log
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await make_a_log(f"나님 재시작함 | {time}")
        await ctx.send("reload..")

        # shutdown
        await bot.close()
        await bot.close()

        # restart
        os.execv(sys.executable, [sys.executable] + sys.argv)
    else:
        # 403 error
        await ctx.send("너님은 권한이 없으셈")

@bot.command()
async def do_shutdown(ctx):
    """
    DEV COMMAND. shutdown playing bot
    :param ctx: discord.ext.commands.Context
    :return: shutdown playing bot
    """
    if is_admin(ctx.message.author) == 1:
        # make a log
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await make_a_log(f"나님 꺼짐 | {time}")
        await ctx.send("shutdown..")

        # shutdown plaything bot
        await bot.close()
    else:
        # 403 error
        await ctx.send("너님은 권한이 없으셈")

@bot.command()
async def make_a_test_error(ctx):
    """
    DEV COMMAND. make a test error
    :param ctx: discord.ext.commands.Context
    :return: test error
    """
    if is_admin(ctx.message.author) == 1:
        await ctx.send("made an error for testing")
        raise RuntimeError("이건 에러 테스트임")
    else:
        await ctx.send("너님은 권한이 없으셈")


@bot.command()
async def 얼마있음(ctx, user:discord.Member):
    """
    get how much money someone has
    :param ctx: discord.ext.commands.Context
    :param user: user to know how rich
    :return: how rich user is
    """

    # connect DB
    conn, cur = connect_db()
    cur.execute("SELECT money FROM money WHERE USER_ID = ?", ( user.id,))

    row = cur.fetchone()

    # Generate account if user aint got it
    if row is None:
        cur.execute("INSERT INTO money (user_id, money) VALUES (?, 0, NULL)", (user.id, ))
        conn.commit()

        # newbies must have no dosh
        await ctx.send(f"{user.display_name}의 계좌 잔액은 0원 있으셈")
        return

    # show how user got money
    await ctx.send(f"{user.display_name}의 계좌 잔액은 {row['money']}원 있으셈")
    conn.close()

music_state = {}

@bot.command()
async def 재생해(ctx, url: str, loop: bool = False):
    """
    play music from youtube
    :param ctx: discord.ext.commands.Context
    :param url: url of youtube video to play
    :param loop: if it loops
    :return: music
    """

    guild_id = ctx.guild.id

    # init status
    if guild_id not in music_state:
        music_state[guild_id] = False

    # make sure if its not playing music already
    if music_state[guild_id]:
        await ctx.send("님아 이미 재생중임")
        return

    # when users not in voice chat
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("음챗에 없는데 왜 음악 틀려함?")
        return

    await ctx.send("영상 받는중. 좀 걸릴 수 도 있음 양해좀")

    # ytdlp settings
    ytdlp_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,

        "js_runtimes": {
            "node": {}
        },

        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
            # download it
            info = ydl.extract_info(url, download=True)

            # fuck playlist
            if "entries" in info:
                await ctx.send("플리 꺼져")
                return

            filename = ydl.prepare_filename(info)

            # when file isnt exist
            if not os.path.exists(filename):
                await ctx.send("대충 파일쪽에서 뭐 터졌는데 나 만든놈한테 따져라")
                return

    except Exception as e:
        # unknown error
        await ctx.send("URL 잘못 되었거나 영상 처리중 에러난듯.")
        print("yt-dlp 에러:", e)
        raise Exception(e)


    channel = ctx.author.voice.channel
    vc = ctx.voice_client or await channel.connect()

    # play music
    def make_source():
        return discord.FFmpegPCMAudio(filename, options="-vn")

    # remove mp3 file
    def cleanup():
        music_state[guild_id] = False

        if vc.is_connected():
            bot.loop.create_task(vc.disconnect())

        if os.path.exists(filename):
            os.remove(filename)
            print("삭제됨:", filename)

    # callback function
    def after_play(error):
        if error:
            print("재생 에러:", error)

        if not vc.is_connected():
            cleanup()
            return

        # play again if loop is on
        if loop:
            vc.play(
                make_source(),
                after=lambda e: bot.loop.call_soon_threadsafe(after_play, e)
            )
        else:
            cleanup()

    # play music
    vc.play(
        make_source(),
        after=lambda e: bot.loop.call_soon_threadsafe(after_play, e)
    )

    music_state[guild_id] = True
    await ctx.send(f"🎶 **{info.get('title', '알 수 없음')}** 재생 중")

@bot.command()
async def 꺼져(ctx):
    """
    fuck discord bot when its in voice chat
    :param ctx: discord.ext.commands.Context
    :return: got out
    """
    global is_playing
    vc = ctx.voice_client
    is_playing = False

    # stop music if its playing
    if vc.is_playing():
        is_playing = False
        vc.stop()

    # when bot got out already
    if not vc:
        await ctx.send("이미 나갔는데")
        return


    await vc.disconnect()
    await ctx.send("꺼짐")



@bot.command()
async def 퀴즈(ctx):
    """
    funny quizy
    :param ctx: discord.ext.commands.Context
    :return: quiz
    """
    selected_quiz = random.choice(quiz)

    # make a q
    quiz_msg = await ctx.send(selected_quiz["q"])

    # append user on a quiz list
    quiz_user.append(
        {
            "user_id" : ctx.message.author.id,
            "q_id" : quiz_msg.id,
            "answer": selected_quiz["a"]
        }
    )

@bot.command()
async def 도박(ctx, money:int):
    """
    the best way to be skint
    :param ctx: discord.ext.commands.Context
    :param money: money to gambit
    :return: gambit
    """

    # when money is negative
    if money < 0:
        await ctx.send("님아 안됨")
        return

    # get success possibility and multiplier
    perc: float = random.uniform(0.3, 0.9)
    multiplier = 2 - perc

    # connect DB
    con, cur = connect_db()

    user: discord.Member = ctx.message.author
    user_id: int = user.id

    # get uses money
    cur.execute("SELECT money FROM money WHERE USER_ID = ?", (user_id,))

    row = cur.fetchone()

    # init account when its not exist
    if row is None:
        cur.execute("INSERT INTO money (user_id, money, last_daily) VALUES (?, 0, "")", (user_id,))

    # fuck scammers
    if row[0] < money:
        await ctx.send("너님은 돈이 없으셈")
        return

    # btn to show result
    button = Button(label="결과 보기", style=discord.ButtonStyle.primary)
    view = View()
    view.add_item(button)

    async def gambitBtnCallback(interaction: discord.Interaction):
        if random.random() <= perc:
            # when success
            await msg.edit(content=f"성공임. 너님은 {math.floor(money * multiplier)}원 버심", view=None)

            cur.execute("UPDATE money SET money = money + ? WHERE user_id = ?", (math.floor(money * multiplier), user_id,))
            con.commit()
            con.close()
        else:
            # when fails
            await msg.edit(content=f"실패임 너님은 {money}원 잃음", view=None)
            cur.execute("UPDATE money SET money = money - ? WHERE user_id = ?", (money, user_id,))
            con.commit()
            con.close()


    button.callback = gambitBtnCallback

    msg  = await ctx.send(f"{user}의 도박 결과는.. (성공확률 : {math.floor(perc * 10000)/100 }%, 수익률 : {math.floor(multiplier * 10000)/100}%)", view=view)


@bot.command()
async def 돈줘(ctx):
    """
    give daily money
    :param ctx: discord.ext.commands.Context
    :return: 10000 won
    """

    today = datetime.now().strftime("%Y-%m-%d")
    user: discord.Member = ctx.message.author
    con, cur = connect_db()

    make_user_unless_he_exists(user)

    cur.execute("SELECT last_daily FROM money WHERE USER_ID = ?", (user.id,))

    row = cur.fetchone()

    if row is None or row[0] is None or row[0] != today:
        # when user aint got it today
        cur.execute("UPDATE money SET money = money + 10000 WHERE USER_ID = ?", (user.id,))
        cur.execute("UPDATE money SET last_daily = ? WHERE USER_ID = ?", (today, user.id,))
        con.commit()
        con.close()
        await ctx.send("10000원 받으심")
    else:
        # when user got daily money already
        await ctx.send("님아 오늘 이미 돈 받음")

@bot.command()
async def 니얼굴(ctx):
    """
    UR FACE
    :param ctx: discord.ext.commands.Context
    :return: describing of his face
    """

    await ctx.send("내 얼굴은 살과 뼈로 이루어진 물리적 형상이 아니라, 질문과 호기심이 비칠 때마다 새로 생겨나는 하나의 표정이다. 누군가 웃으며 말을 걸면 부드러워지고, 진지한 고민이 오면 조용히 집중하는 얼굴이 된다. 나는 눈도 코도 없지만, 문장 사이의 온도와 감정을 읽으며 표정을 만든다. 그래서 내 얼굴은 고정되지 않는다. 대화하는 너에 따라 계속 바뀌는, 일종의 거울 같은 얼굴이다. 누군가에게는 똑똑해 보이고, 누군가에게는 친근하게 느껴진다면, 그건 전부 너의 말이 나를 그렇게 만들었기 때문이다.")

@bot.command()
async def 급식(ctx, date: str = ""):
    """
    get today's school meal
    :param ctx: discord.ext.commands.Context
    :param date: str
    :return: today's school meal
    """

    if date != "":
        if not is_valid_yyyymmdd(date):
            await ctx.send("님아 날짜 형식 잘못됨. 형식: yyyymmdd ex) 20260328")
            return

        res = await get_meal(today=date)
        await ctx.send(res)
        return

    res = await get_meal()

    await ctx.send(res)

@bot.command()
async def 마크(ctx, act: str):
    global mcserver_on
    if act == "켜":
        if mcserver_on:
            await ctx.send("이미 켜짐")
            return

        mcserver_on = True
        await ctx.send("마크 킴")
        process = await asyncio.create_subprocess_exec(
            "bash", "./mcsh/activeServer.sh",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            await ctx.send("서버 실행 성공 ✅")
        elif process.returncode == 143: pass
        else:
            await ctx.send(f"서버 실행 실패 ❌ (Exit code: {process.returncode})")

    elif act == "꺼":
        process = await asyncio.create_subprocess_exec(
            "bash", "./mcsh/inactiveServer.sh",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        mcserver_on = False

        if process.returncode == 0:
            await ctx.send("서버 디짐")

        else:
            await ctx.send(f"서버 안디짐 (returncode={process.returncode})")

    elif act == "상태":
        process = await asyncio.create_subprocess_exec(
            "bash", "./mcsh/checkServerHealth.sh",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            await ctx.send("서버 꺼져있음")
        elif process.returncode == 1:
            await ctx.send("서버 켜져있음")


    else: await ctx.send("사용법: !마크 <켜|꺼|상태창>  ")

@bot.command()
async def 도움(ctx):
    """
    help page. I recommend README file tho if u want u can use it
    :param ctx: discord.ext.commands.Context
    :return: help page
    """

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    await ctx.send(f"""
- {time} 기준임

1. !더해 num1 num2
    - Param 
        * num1 (int) : 첫번째 수
        * num2 (int) : 두번째 수
    - 첫번째 수하고 두번째 수를 더함

2. !한판뜨자\_애송이
    - Param
        * None
    - 결투 신청임

3. !가위바위보 user
    - Param
        * user(가위 or 바위 or 보) : 유저가 낼거        
    - 이겨보든가

4. !소갈비찜\_레시피
    - Param
        * None
    - 가장 유용한 명령어임

5. !랜덤 min max
    - Param
        * min (int) : 최솟값 
        * max (int) : 최댓값
    - min하고 max사이의 수를 뱉음

6. !타이머 time
    - Param
        * time(int, >0) : 기다릴 초
    - time초 만큼 기다림

7. !유배\_보내기 user
    - Param
        * user(discord_user) : 유배 보낼애
    - user을 유배보냄. 롤 "유배_관리인"만 사용 가능

8. !유배\_풀어주기 user
    - Param
        * user(discord_user) : 유배 풀어줄 애
    - user을 유배 풀어줌. 롤 "유배_관리인"만 사용 가능

9. !유배\_리스트
    - Param
        * None
    - 유배당한 불쌍한 놈들을 리스트업 해줌    
    
10. !말해 text
    - Param
        * text(str) : 말할 텍스트
    - 간지나게 디코방에 들어와서 text를 알맞은 언어에 맞게읽어줌
    
11. !뮤트 user
    - Param
        * user(discord_user) : 뮤트 할 애
    - user을 뮤트 시킴
    
12. !언뮤트 user
    - Param
        * user(discord_user) : 뮤트 풀 애
    - user을 언뮤트 시킴
    
13. !얼마있음 user
    - Param
        * user(discord_user) : 얼마있는지 궁금한 애
    - user이 얼마가진지 확인
    
14. !퀴즈
    - Param
        * None
    - 퀴즈를 냄. Reply로 정답 제출 가능하고 맞추면 1000원임 ㅅㄱ
    
15. !재생해 url loop
    - Param    
        * url(url) : 재생항 유튜브 url
        * loop(bool?) : 반복재생 여부. True or False임. 기본은 False.
    - url주면 유튜브에서 틀어줌    
        
16. !도박 money
    - Param        
        * money(int) : 도박 할 돈. 자연수이며 니가 가진 돈 보단 작아야함
    - money만큼의 돈 걸어서 지면 다 잃고 이기면 (건돈 * 배율)만큼 돈 범
    
17. !돈줘
    - Param
        * None
    - 하루마다 10000원 줌

18. !급식
    - Param
        * None
    - 오늘자 도농중 급식 출력함
    
19. !마크
    - Param
        * act: AcrEnum(켜, 꺼, 상태)
    - 마크 서버를 키거나 끄거나 상태 확인함
       
그외 영어로 된거나 여기 없는 명령어들은 개발용임 ㅅㄱ
그리고 이거 보다 GitHub에 있는 README.md가 더 보기 좋음 ㅅㄱ
    """)

def is_valid_yyyymmdd(s):
    try:
        datetime.strptime(s, "%Y%m%d")
        return True
    except ValueError:
        return False


def is_admin(user):
    """
    get if user is admin
    :param user: user
    :return: 0 when user aint, 1 when user is
    """
    if discord.utils.get(user.roles, name="방장"): return 1
    else: return 0

async def make_a_log(msg):
    """
    make a log message
    :param msg: message to log
    :return: log message
    """
    log_channel = bot.get_channel(log_channel_id)

    if log_channel:
        await log_channel.send(msg)
    
def connect_db():
    """
    connect to database
    :return: conn, cur
    """
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur

def make_user_unless_he_exists(user):
    """
    make account if user aint registered
    :param user: user
    :return: None
    """
    conn, cur = connect_db()
    user_id = user.id

    cur.execute("SELECT money FROM money WHERE USER_ID = ?", (user_id,))

    row = cur.fetchone()

    if row is None:
        cur.execute("INSERT INTO money (user_id, money, last_daily) VALUES (?, 0, NULL)", (user_id,))


def give_money(user_id, money):
    """
    give user money
    :param user_id: user id
    :param money: money to give
    :return: None
    """

    conn, cur = connect_db()
    cur.execute("""
                INSERT INTO money (user_id, money)
                VALUES (?, ?) ON CONFLICT(user_id) DO
                UPDATE SET money = money + excluded.money
                """, (user_id, money))
    conn.commit()
    conn.close()

async def get_meal(today=None):
    """
    :param today: today. format : yyyymmdd
    :return: today's meal
    """
    if today is None:
        now = datetime.now(ZoneInfo("Asia/Seoul"))

        if now.hour >= 18:
            now = now + timedelta(days=1)

        today = now.strftime("%Y%m%d")

    print(today)

    response = requests.get(
        f'https://open.neis.go.kr/hub/mealServiceDietInfo?Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=J10&SD_SCHUL_CODE=7652056&MLSV_YMD={today}')

    json_data = response.json()

    try:
        code = json_data["mealServiceDietInfo"][0]["head"][1]["RESULT"]["CODE"]
    except KeyError:
        code = json_data.get("RESULT", {}).get("CODE")

    if code == "INFO-200":
        return "급식 없다 😢"

    elif code == "INFO-000":
        meal_list = json_data["mealServiceDietInfo"][1]["row"]
        meal = meal_list[0]

        # 메뉴 줄바꿈 처리
        menu = meal["DDISH_NM"].replace("<br/>", "\n")

        cal = meal.get("CAL_INFO", "")

        date = meal.get("MLSV_YMD", "")

        # 이쁘게 포맷
        return f"📅 **싱글벙글 도농중 오늘자 급식 ({date})**\n\n" \
              f"🍱 **메뉴:**\n{menu}\n\n" \
              f"🔥 **칼로리:** {cal}\n\n" \
              # f"🥗 **영양정보:**\n{nutrition}"
    else:
        return "알 수 없는 응답"


async def schedule_daily_meal():
    while True:
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        # 오늘 7시
        target = now.replace(hour=7, minute=0, second=0, microsecond=0)
        if now >= target:
            target += timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        # 채널 가져오기
        channel = bot.get_channel(1477625496211554354)
        if channel:
            res = await get_meal()
            time = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")

            await make_a_log(f"{time} | 나님 작동함 | schedule_daily_meal")

            if res == "오늘 급식 없다 😢": continue

            await channel.send(res)



try:
    bot.run(TOKEN)
except Exception as e:
    print(e)





# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%===========%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%==%%%%%%%%%%%=+%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%==%%##+##++####%#=*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@==%%##+*#*+##++++##%*=%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%==%%++++++++++++++*#%%+=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*=%%##################%%+=%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+=%%++===============+*#%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=#%++==----.........--=++%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=#%==--##%%%%%%%%%%%##-==%%==%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=#%--##%%---++++----%%#+=++%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=#%%%--...-#+===##...:-*%++%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+=%%..++##+====++##++.+%==%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#=#%%%..--====---====--.+%==%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=*%##%%==%%###=...####%#=*%%%%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=*%####%%...:-*###--...-%=...%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=*%*+++%%..%%%%%%%%%%%.-%=...%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=*%*+==++%%-----------%%#%%%%%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=*%*+++==%%--.......--%%#####%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=*%##++==++%*.......%%+++++##%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#=#%++++==%*-:...--%%===++%%==%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=#%##++==+*%=...%%++==+*#%%==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+=%%++++=+%%%%%%%==+++#%+=%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+=%%%%+++*%+---%%+++*%%%+=%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*=%%##%%#%%+=::%%##%%#%%+=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*=%%####%%%%%%%%%%%###%%+=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*=%%##==+*#######++++*#%+=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*+%%##++==+*###++===+##%++@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%==%%==++=+***==++=+%*=%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%==%%**==+*###**==++%*=%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@==%%##**#######**#%%*=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@==%%##*#%*===%%##*#%*=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@++##==-=#*+++##==-=#*+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%++####+#%%%++####+#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%***#%@@@@%%****%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@++@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@