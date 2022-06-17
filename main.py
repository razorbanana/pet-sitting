import pymysql
from config import host, user, password, db_name

#moderator menu
def showHistMd(id, user_id):
    print("Request history:")
    sql = "SELECT u.id as `user id`,CONCAT(`first_name`,' ',`last_name`) as `owners name`,`city`,`price`, `description`,`review`,`rating`, `name`, `info` FROM ((`pet_list` as p JOIN `request_history` as r on (p.id = r.pet_id)) JOIN `user_list` as u on (u.id = p.owner_id)) JOIN `status` as s on (r.status_id = s.id) WHERE closed = 1 and owner_id = %s"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchall()
    if len(result) == 0:
        print("No requests")
    for i in result:
        for key, value in i.items():
            print(key, ' : ', value)
        print("\n")
    n = input("1.Moderate requests\n2.Menu\nInput number:")
    if n == '1':
        modReq(id)
    elif n == '2':
        menuMd(id)
    else:
        print("Wrong input, open menu")
        modReq(id)

def modReq(id):
    print("Request list:")
    sql = "SELECT r.id as `request id`, u.id as `user id`,CONCAT(`first_name`,' ',`last_name`) as `owners name`,`city`,`price`, `description`, p.name, `info` FROM (`pet_list` as p JOIN `request_list` as r on (p.id = r.pet_id)) JOIN `user_list` as u on (u.id = p.owner_id) WHERE  status_id = 1 AND petsittler_id is NULL"
    cursor.execute(sql, ())
    result = cursor.fetchall()
    if len(result) == 0:
        print("No requests")
    for i in result:
        for key, value in i.items():
            print(key, ' : ', value)
        print("\n")
    n = input("1.Accept/delete request\n2.Show request history\n3.Menu\nInput number:")
    if n == '1':
        n = input("Input id of request:")
        flag = input("0 for delete request, 1 for accept request:")
        if flag == '0':
            sql = "CALL delete_request_list(%s)"
            cursor.execute(sql, (n))
            connection.commit()
        elif flag == '1':
            sql = "CALL update_request_list_status(%s,%s)"
            cursor.execute(sql, (2, n))
            connection.commit()
        else:
            print("Wrong input, try again")
            modReq(id)
        print("Moderate request:")
        modReq(id)
    elif n == '2':
        n = input("Input user id:")
        showHistMd(id, n)
    elif n == '3':
        menuMd(id)
    else:
        print("Wrong input, open menu")
        menuMd(id)

def menuMd(id):
    n = input("1. Ban User\n2. Moderate request\n3. Log out\nInput number:")
    if n == '1':
        banUser(id)
    elif n == '2':
        modReq(id)
    elif n == '3':
        start()
    else:
        print("Wrong input, try again")
        menuMd(id)
#end moderator menu

#admin menu
def giveRoutes(id):
    print("User list:")
    sql = "SELECT `id`,CONCAT(`first_name`,' ',`last_name`) as `name`, `email`,`phone`,`role` FROM `user_list` WHERE `role` != 'admin'"
    cursor.execute(sql, ())
    result = cursor.fetchall()
    for i in result:
        for key, value in i.items():
            print(key, ' : ', value)
        print("\n")
    n = input("1. Return to menu\n2. Give routs\nInput number:")
    if n == '1':
        menuAd(id)
    elif n == '2':
        n = input("Input users id:")
        role = input("Input new role (1 - user, 2 - manager):")
        sql = "CALL update_user_list_role(%s,%s)"
        cursor.execute(sql, (role,n))
        connection.commit()
        giveRoutes(id)
    else:
        print("Wrong number, direct to menu")
        menuAd(id)

def banUser(id):
    print("User list:")
    sql = "SELECT `id`,CONCAT(`first_name`,' ',`last_name`) as `name`, `email`,`phone`,`role` FROM `user_list` WHERE `role` = 1"
    cursor.execute(sql, ())
    result = cursor.fetchall()
    for i in result:
        for key, value in i.items():
            print(key, ' : ', value)
        print("\n")
    n = input("1. Return to menu\n2. Ban/unban user\nInput number:")
    if n == '1':
        menuAd(id)
    elif n == '2':
        n = input("Input users id:")
        m = int(input("0 for ban, 1 for unban:"))
        if m not in [0, 1]:
            print("Wrong input, try again")
            banUser(id)
        sql = "CALL update_user_list_enabled(%s,%s)"
        cursor.execute(sql, (m,n))
        connection.commit()
        banUser(id)
    else:
        print("Wrong number, direct to menu")
        menuAd(id)

def menuAd(id):
    n = input("1. Give Routs\n2. Delete users\n3. Log out\nInput number:")
    if n == '1':
        giveRoutes(id)
    elif n == '2':
        banUser(id)
    elif n == '3':
        start()
    else:
        print("Wrong input, try again")
        menuAd(id)
#end admin menu

#user menu
def accReq(id):
    print("Accepted requests:")
    sql = "SELECT CONCAT(`first_name`,' ',`last_name`) as `owners name`,`city`,`price`, `description`, p.name as `pets name`, p.info as `pets info`, s.name as `status` FROM ((`pet_list` as p JOIN `request_list` as r on (p.id = r.pet_id)) JOIN `user_list` as u on (u.id = p.owner_id)) JOIN `status` as s on (r.status_id = s.id) WHERE r.petsittler_id = %s"
    cursor.execute(sql, (id,))
    result = cursor.fetchall()
    for i in result:
        for key, value in i.items():
            print(key, ' : ', value)
        print("\n")
    n = input("1. Return to menu\n2. Accept request\nInput number:")
    if n == '1':
        menu(id)
    elif n == '2':
        showReq(id)
    else:
        print("Wrong number, open menu")
        menu(id)

def settings(id):
    n = input("1. Change name\n2. Change city\n3. Menu\nInput number:")
    if n =='1':
        fn = input("Input your new first name:")
        sn = input("Input your new second name:")
        sql = "CALL update_user_list_name(%s,%s,%s)"
        cursor.execute(sql, (fn, sn, id))
        connection.commit()
        settings(id)
    if n == '2':
        city = input("Input your new city:")
        sql = "CALL update_user_list_city(%s,%s)"
        cursor.execute(sql, (city, id))
        connection.commit()
        settings(id)
    if n == '3':
        menu(id)

def showPet(id):
    print("Pet list:")
    sql = "SELECT `name`, `species`,`info` FROM `pet_list` WHERE owner_id = %s"
    cursor.execute(sql, (id,))
    result = cursor.fetchall()
    for i in result:
        for key, value in i.items():
            print(key, ' : ', value)
        print("\n")
    n = input("1. Return to menu\n2. Add pet\nInput number:")
    if n == '1':
        menu(id)
    elif n == '2':
        insertPet(id)

def insertPet(id):
    name = input("Input name of your pet:")
    if len(name) > 32:
        print("Too long name, try again")
        insertPet(id)
    species = input("Input species of your pet:")
    if len(species) > 20:
        print("Too long input, try again")
        insertPet(id)
    info = input("Input info about your pet:")
    if len(info) > 200:
        print("Too long info, try again")
        insertPet(id)
    sql = "CALL insert_pet_list(%s,%s,%s,%s)"
    cursor.execute(sql, (id, name, species, info))
    connection.commit()
    n = input("1. Add pet\n2. Show pet list\n3. Menu\nInput number:")
    if n == '1':
        insertPet(id)
    elif n == '2':
        showPet(id)
    elif n == '3':
        menu(id)
    else:
        print("Wrong input, open menu")
        menu(id)

def showHist(id, user_id):
    print("Request history:")
    sql = "SELECT u.id as `user id`,CONCAT(`first_name`,' ',`last_name`) as `owners name`,`city`,`price`, `description`,`review`,`rating`, p.name, `info` FROM ((`pet_list` as p JOIN `request_history` as r on (p.id = r.pet_id)) JOIN `user_list` as u on (u.id = r.petsittler_id)) JOIN `status` as s on (r.status_id = s.id) WHERE s.closed = 1 and r.petsittler_id = %s"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchall()
    if len(result) == 0:
        print("No requests")
    for i in result:
        for key, value in i.items():
            print(key, ' : ', value)
        print("\n")
    n = input("1.Your requests\n2.Menu\nInput number:")
    if n == '1':
        yourReq(id)
    elif n == '2':
        menu(id)
    else:
        print("Wrong input, open menu")
        menu(id)

def yourReq(id):
    print("Request list:")
    sql = "SELECT r.id,`price`, `description`, p.name, `info`,u.id as `petsitter id`, CONCAT(`first_name`,' ',`last_name`) as `petsitters name`,`phone` FROM (`pet_list` as p JOIN `request_list` as r on (p.id = r.pet_id)) LEFT JOIN `user_list` as u on (u.id = r.petsittler_id) WHERE p.owner_id = %s"
    cursor.execute(sql, (id,))
    result = cursor.fetchall()
    for i in result:
        for key, value in i.items():
            print(key, ' : ', value)
        print("\n")
    n = input("1. Moderate requests\n2. End Request\n3. Show request history of user\n4. Return to menu\n5. Make new request\nInput number:")
    if n == '1':
        n = input("Input id of request:")
        m = input("Input 1 if accept, 2 if reject:")
        if m == '1':
            sql = "CALL update_request_list_status(%s,%s)"
            cursor.execute(sql, (4, n))
            connection.commit()
        elif m == '2':
            sql = "CALL update_request_list_petsitter(%s,%s)"
            cursor.execute(sql, (None, n))
            connection.commit()
        else:
            print("Wrong input, try again")
            yourReq(id)
        print("Menu:")
        menu(id)
    elif n == '2':
        n = input("Input id of request:")
        sql = "SELECT `status_id` FROM  `request_list` WHERE id = %s"
        cursor.execute(sql, (n,))
        result = cursor.fetchone()
        if result['status_id'] == 4:
            review = input("Input your review (<200 char):")
            if len(review) > 200:
                print("Wrong input, try again")
                yourReq(id)
            rating = int(input("Input your rating (1-5):"))
            if rating not in [1,2,3,4,5]:
                print("Wrong input, try again")
                yourReq(id)
            sql = "CALL update_request_list_status(%s,%s)"
            cursor.execute(sql, (5, n))
            connection.commit()
            sql = "CALL insert_request_history_from_list(%s,%s,%s)"
            cursor.execute(sql, (review, rating, n))
            connection.commit()
            sql = "CALL delete_request_list(%s)"
            cursor.execute(sql, (n))
            connection.commit()
        else:
            sql = "CALL delete_request_list(%s)"
            cursor.execute(sql, (n))
            connection.commit()
        print("Menu:")
        menu(id)
    elif n == '3':
        n = input("Input user id:")
        showHist(id, n)
    elif n == '4':
        menu(id)
    elif n =='5':
        makeReq(id)
    else:
        print("Wrong number, open menu")
        menu(id)

def makeReq(id):
    price = float(input("Input price:"))
    if price > 1000:
        print("Wrong price, try again:")
        makeReq(id)

    desc = input("Input description:")
    if len(desc) > 200:
        print("Wrong description, try again:")
        makeReq(id)

    print("Choose your pet:")
    sql = "SELECT `id`, `name` FROM `pet_list` WHERE owner_id = %s"
    cursor.execute(sql, (id,))
    result = cursor.fetchall()
    for i in result:
        for key, value in i.items():
            print(key, ' : ', value)
        print("\n")
    if len(result) == 0:
        print("You have not pet, add pet")
        insertPet(id)
    petId = input("Input chosen pet`s id:")
    sql = "CALL insert_request_list(%s,%s,%s,%s)"
    cursor.execute(sql, (price, desc, petId, id))
    connection.commit()
    n = input("1. Your requests\n2. Make new request\n3. Menu\nInput number:")
    if n == '1':
        yourReq(id)
    elif n == '2':
        makeReq(id)
    elif n == '3':
        menu(id)
    else:
        print("Wrong input, open menu")
        menu(id)

def showReq(id):
    print("Request list:")
    sql = "SELECT r.id,CONCAT(`first_name`,' ',`last_name`) as `owners name`,`city`,`price`, `description`, `name`, `info` FROM (`pet_list` as p JOIN `request_list` as r on (p.id = r.pet_id)) JOIN `user_list` as u on (u.id = p.owner_id) WHERE p.owner_id != %s AND status_id = 2 AND petsittler_id is NULL AND u.enabled = 1 ORDER BY (SELECT `city` FROM user_list WHERE id = %s) = city DESC"
    cursor.execute(sql, (id,id))
    result = cursor.fetchall()
    if len(result) == 0:
        print("No requests")
    for i in result:
        for key, value in i.items():
            print(key, ' : ', value)
        print("\n")
    n = input("1.Accept request\n2.Menu\nInput number:")
    if n == '1':
        n = input("Input id of request:")
        sql = "CALL update_request_list_petsitter(%s,%s)"
        cursor.execute(sql, (id, n))
        connection.commit()
        print("Menu:")
        menu(id)
    elif n == '2':
        menu(id)
    else:
        print("Wrong input, open menu")
        menu(id)

def menu(id):
    n = input("1. Make request\n2. Show requests\n3. Your requests\n4. Your pets\n5. Add pet\n6. Account settings\n7. Accepted requests\n8. Log out\nInput:")
    if n == '1':
        makeReq(id)
    elif n == '2':
        showReq(id)
    elif n == '3':
        yourReq(id)
    elif n == '4':
        showPet(id)
    elif n == '5':
        insertPet(id)
    elif n == '6':
        settings(id)
    elif n == '7':
        accReq(id)
    elif n == '8':
        start()
    else:
        print("Wrong number, try again")
        menu(id)
#end user menu

#login
def login():
    print("Login")
    user_name = input("Input login:")
    key = input("Input password:")
    sql = "SELECT id,role,enabled FROM `user_list` WHERE `login`=%s AND TO_BASE64(AES_ENCRYPT(%s,'stas')) = `password`"
    cursor.execute(sql, (user_name, key,))
    result = cursor.fetchone()
    print(result)
    if result is None:
        print("Wrong input, try again:")
        start()
    else:
        print(result['id'])
        if result['role'] == 'user':
            if result['enabled'] == 0:
                print("You are banned.")
                start()
            else:
                menu(result['id'])
        elif result['role'] == 'manager':
            menuMd(result['id'])
        elif result['role'] == 'admin':
            menuAd(result['id'])

def reg():
    print("Register")
    user_name = input("Input login (6-16 characters):")
    if len(user_name) > 16 or len(user_name) < 6:
        print("Wrong login, try again:")
        start()
    sql = "SELECT `id` FROM `user_list` WHERE `login`=%s "
    cursor.execute(sql, (user_name,))
    result = cursor.fetchone()
    if result is not None:
        print("Wrong input, try again:")
        start()

    fn = input("Input first name (2-15 characters):")
    if len(fn) > 15 or len(fn) < 2:
        print("Wrong first name, try again:")
        start()

    sn = input("Input second name (2-15 characters):")
    if len(sn) > 15 or len(sn) < 2:
        print("Wrong second name, try again:")
        start()

    email = input("Input email:")
    if len(email) > 319 or len(email) < 2:
        print("Wrong email, try again:")
        start()
    sql = "SELECT `id` FROM `user_list` WHERE `email`=%s "
    cursor.execute(sql, (email,))
    result = cursor.fetchone()
    if result is not None:
        print("Wrong input, try again:")
        start()

    phone = input("Input phone (+...):")
    if len(phone) != 13:
        print("Wrong phone number, try again:")
        start()

    key = input("Input password (6-16):")
    if len(key) > 16 or len(key) < 6:
        print("Wrong password, try again:")
        start()

    city = input("Input city:")
    if len(city) > 20:
        print("Wrong city, try again:")
        start()

    birth_date = input("Input birth date (YYYY-MM-DD):")
    if len(birth_date) != 10:
        print("Wrong birth date, try again:")
        start()

    sql = "CALL insert_user_list(%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (user_name, fn, sn, email, phone, key, city, birth_date))
    connection.commit()
    login()

def start():
    n = input("1. Login\n2. Register\nInput:")
    if n == '1':
        login()
    elif n == '2':
        reg()
    else:
        print("Wrong number, try again")
        start()
#end login

# start
try:
    connection = pymysql.connect(host=host,
                                 port=3306,
                                 user=user,
                                 password=password,
                                 database=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print("Connected")
    try:
        with connection.cursor() as cursor:
            start()
    finally:
        connection.close()
except Exception as ex:
    print("Connection refused")
    print(ex)
