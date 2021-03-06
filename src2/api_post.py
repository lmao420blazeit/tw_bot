# post api

"""
class API_get:



    _instance = BaseAPI()


    def __init__(self):
        self.session = API_get._instance.session
        self.gameworld = API_get._instance.gameworld
        self.csrf_token = API_get._instance.csrf_token
        self.session_id = API_get._instance.session_id
        self.time = time.time()

    def premium_features(self, village_id:str) -> dict:

        """ {
              'Premium': {
                'possible': True,
                'active': True
              },
              'AccountManager': {
                'possible': True,
                'active': True
              },
              'FarmAssistent': {
                'possible': True,
                'active': True
              }
            } 
        """

        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=api&ajax=resources_schedule&id={village_id}&client_time={self.time}"

        with self.session as ses:

            res  = ses.get(url).json()["game_data"]['features']
            return(res) # done

    def player_info(self, village_id: str) -> dict:

        """ {
              'id': '237776',
              'name': 'Seelfed',
              'ally': '1805',
              'ally_level': '10',
              'ally_member_count': '40',
              'sitter': '0',
              'sleep_start': '0',
              'sitter_type': 'normal',
              'sleep_end': '0',
              'sleep_last': '0',
              'email_valid': '1',
              'villages': '59',
              'incomings': '0',
              'supports': '0',
              'knight_location': '25248',
              'knight_unit': '610842885',
              'rank': 144,
              'points': '440086',
              'date_started': '1532186125',
              'is_guest': '0',
              'birthdate': '0000-00-00',
              'confirmation_skipping_hash': '',
              'quest_progress': '0',
              'points_formatted': '440<span class="grey">.</span>086',
              'rank_formatted': '144',
              'pp': '1377',
              'new_ally_application': '0',
              'new_ally_invite': '0',
              'new_buddy_request': '0',
              'new_daily_bonus': '0',
              'new_forum_post': '3',
              'new_igm': '0',
              'new_items': '2',
              'new_report': '0',
              'new_quest': '1'
            } 
        """

        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=api&ajax=resources_schedule&id={village_id}&client_time={self.time}"

        with self.session as ses:

            res  = ses.get(url).json()["game_data"]["player"]
            return(res) # done

    def number_of_villages(self, village_id:str) -> dict:

        """ tested with premium
            returns {village_id, village_name} """

        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=overview_villages"

        def parser(url:str):
            village_id = []
            village_name = []
            soup = BeautifulSoup(url, 'html.parser')
            now = list(soup.find_all(attrs={'class': 'quickedit-vn'}))
            for element in now:
                village_id.append(element["data-id"])
            then = list(soup.find_all(attrs={'class': 'quickedit-label'}))
            for element in then:
                village_name.append(element["data-text"])

            villages = dict(zip(village_id, village_name))
            return(villages)

        with self.session as ses:
            res = ses.get(url)
            parser(res.text) # done

    def incoming(self, village_id:str) -> list:

        """ tested with premium
            returns {village_id, village_name} 
            [{'from': '004 ~ Hyper (481|655) K64', 'to': '028 ~ Tighten Up (484|664) K64', 'from_player': 'Seelfed', 'distance': '9.5', 'duration': '0:23:58'}, 
            {'from': '004 ~ Hyper (481|655) K64', 'to': '036 ~ chamk (482|666) K64', 'from_player': 'Seelfed', 'distance': '11.0', 'duration': '0:37:46'},  
            {'from': '004 ~ Hyper (481|655) K64', 'to': '036 ~ chamk (482|666) K64', 'from_player': 'Seelfed', 'distance': '11.0', 'duration': '0:37:54'}, 
            {'from': '004 ~ Hyper (481|655) K64', 'to': '040 ~ FIlIPE95 (473|675) K64', 'from_player': 'Seelfed', 'distance': '21.5', 'duration': '1:41:02'}, 
        """

        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=overview_villages&mode=incomings&subtype=attacks"

        def parser(url:str):

            lista = []
            soup = BeautifulSoup(url, 'html.parser')
            now = soup.find_all(attrs={'class': 'quickedit'})
            for element in now:
                element = element.find_parent("tr")
                ele = element.find_all("td")
                timer = element.find(attrs = {'class': 'timer'}).text
                element = list(element.find_all("a"))
                att = ({"from": element[3].text, "to": element[2].text, "from_player": element[4].text, "distance": ele[4].text.strip("\n").strip(" "), "duration": timer})
                lista.append(att)

            return(lista)

        with self.session as ses:
            res = ses.get(url)
            return(parser(res.text) )

    ##################          VILLAGE INFORMATION ENDPOINT        ##################  

    def troops_available(self, village_id:str) -> dict:

        """ troops in village and from village
            troops available for new orders
           {'spear': '0', 'sword': '0', 'axe': '3645', 'archer': '0', 'spy': '140', 'light': '1847', 'marcher': '100', 'heavy': '0', 'ram': '220', 'catapult': '61', 'knight': '0', 'snob': '0', 'militia': '0'}
        """

        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=place&mode=units"
        unit_list = ["spear", "sword", "axe", "archer", "spy", "light", "marcher", "heavy", "ram", "catapult", "knight", "snob", "militia"]

        def parser(url:str):
            units = {}
            soup = BeautifulSoup(url, 'html.parser')
            village = soup.find(class_ = "unit-item-spear").find_parent("tr")
            village = list(village.find_all(class_ = "unit-item"))
            count = 0
            for element in village:
                units.update({unit_list[count]: element.text})
                count += 1
            return units 

        with self.session as ses:
            res = ses.get(url).text
            return parser(res)
    
    def attack_power(self, village_id:str) -> dict:

        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=place&mode=units&display=stats_att"
        stats = ["village", "general power", "cavalry power", "archer power"]

        def parser(url:str):
            try:
                attackpower = {}
                soup = BeautifulSoup(url, 'html.parser')
                village = soup.find_all(class_ = "hidden")[1]
                village = village.find_parent("tr")
                count = 0
                for td in village.select('td'):
                    attackpower.update({stats[count]: td.text})
                    count += 1
                attackpower.pop("village")
                return(attackpower)

            except Exception:
                return({})
 

        with self.session as ses:
            res = ses.get(url).text
            parser(res)

        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=overview&ajax=widget&widget=units&client_time={self.time}"
        
        with self.session as ses:
            
            res = ses.get(url).json()["response"]
            return (parser(res)) # deprecated

    def village_info(self, village_id: str) -> dict:

        """ {
              'id': 27802,
              'name': '005 ~ Critical',
              'wood_prod': 1.53333335,
              'stone_prod': 1.53333335,
              'iron_prod': 1.53333335,
              'storage_max': 400000,
              'pop_max': 31363,
              'wood_float': 87056.80737,
              'stone_float': 104001.8074,
              'iron_float': 336208.8074,
              'wood': 87057,
              'stone': 104002,
              'iron': 336209,
              'pop': 31363,
              'x': 481,
              'y': 660,
              'trader_away': 0,
              'bonus_id': '4',
              'bonus': {
                'farm': 1.1,
                'wood': 1.15,
                'stone': 1.15,
                'iron': 1.15
              },
              'buildings': {
                'village': '27802',
                'main': '20',
                'farm': '30',
                'storage': '30',
                'place': '1',
                'barracks': '25',
                'church': '0',
                'church_f': '0',
                'smith': '20',
                'wood': '30',
                'stone': '30',
                'iron': '30',
                'market': '20',
                'stable': '20',
                'wall': '20',
                'garage': '5',
                'hide': '3',
                'snob': '1',
                'statue': '1',
                'watchtower': '0'
              },
              'player_id': '237776',
              'modifications': 1,
              'points': 9742,
              'last_res_tick': 1540988108000.0,
              'res': [
                87057,
                1.53333335,
                104002,
                1.53333335,
                336209,
                1.53333335,
                400000,
                31363,
                31363
              ],
              'coord': '481|660',
              'is_farm_upgradable': False
            } """

        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=api&ajax=resources_schedule&id={village_id}&client_time={self.time}"

        with self.session as ses:

            res  = ses.get(url) #.json()["game_data"]['village']
            return(res.text) # good

    def garage_queue(self, village_id:str) -> dict: # done

        """ returns a list of orders; each order is a dictionary
            [{'Catapulta': {'duration': '4:58:55', 'date_completion': 'amanhã às 03:01:27 horas', 'quantity': 10}}] 
        """
            
        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=garage"

        def parser(url:str) -> dict:

            units = ["Ariete", "Catapulta"]

            soup = BeautifulSoup(url, 'html.parser')

            try:
                orders = []
                # find executing order
                timer = soup.find(id = "trainqueue_wrap_garage")
                timer = list(timer.find_all(attrs = {"class": "lit-item"}))

                queue = soup.find(id = "trainqueue_wrap_garage").find(class_ = "lit-item").text
                for unit in units:
                    if unit in queue:
                        quantity = [int(s) for s in queue.split() if s.isdigit()][0]
                        orders.append({unit:{"duration": timer[1].text, "date_completion": timer[2].text, "quantity": quantity}})

                # find other orders           
                queue = soup.find(id = "trainqueue_garage")

                queue = list(queue.find_all(attrs = {"class": "sortable_row"}))
                for element in queue:
                    lista = (list(element.find_all("td")))
                    for unit in units:
                        if unit in element.text:
                            quantity = [int(s) for s in element.text.split() if s.isdigit()][0]
                            orders.append({unit: {"duration": lista[1].text, "date_completion": lista[2].text, "quantity": quantity}})

                return (orders)

            except AttributeError:
                
                return([]) # return empty list if not training any unit

            except Exception: # for unknown exceptions and other exceptions such as unit not being researched or building not built
                # add log
                return([])

        with self.session as ses:

            res = ses.get(url)
            return parser(res.text) # error when queue is empty

    def stable_queue(self, village_id:str) -> dict: # error when queue is empty

        """ returns the list of orders; each order is a dictionary
            [{'Cavalaria leve': {'duration': '0:16:08', 'date_completion': 'hoje às 20:30:11 horas', 'quantity': 6}}, 
             {'Cavalaria leve': {'duration': '1:02:22', 'date_completion': 'hoje às 21:32:33 horas', 'quantity': 20}}]"""
            
        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=stable"

        def parser(url:str) -> dict:

            units = ["Batedor", "Cavalaria leve", "Arqueiro a cavalo", "Cavalaria Pesada"]

            soup = BeautifulSoup(url, 'html.parser')

            try:
                orders = []
                # find executing order
                timer = soup.find(id = "trainqueue_wrap_stable")
                timer = list(timer.find_all(attrs = {"class": "lit-item"}))

                queue = soup.find(id = "trainqueue_wrap_stable").find(class_ = "lit-item").text
                for unit in units:
                    if unit in queue:
                        quantity = [int(s) for s in queue.split() if s.isdigit()][0]
                        orders.append({unit:{"duration": timer[1].text, "date_completion": timer[2].text, "quantity": quantity}})

                # find other orders           
                queue = soup.find(id = "trainqueue_stable")

                queue = list(queue.find_all(attrs = {"class": "sortable_row"}))
                for element in queue:
                    lista = (list(element.find_all("td")))
                    for unit in units:
                        if unit in element.text:
                            quantity = [int(s) for s in element.text.split() if s.isdigit()][0]
                            orders.append({unit: {"duration": lista[1].text, "date_completion": lista[2].text, "quantity": quantity}})

                return (orders)

            except AttributeError:
                
                return([]) # return empty list if not training any unit

            except Exception: # for unknown exceptions and other exceptions such as unit not being researched or building not built
                # add log
                return([])


        with self.session as ses:

            res = ses.get(url)
            return parser(res.text) # error when queue is empty

    def barracks_queue(self, village_id: str) -> dict: # error when queue is empty

        """ returns list of orders; each order is a dictionary
            [{'Lanceiro': {'duration': '1:06:01', 'date_completion': 'hoje às 15:06:26 horas', 'quantity': 50}}, 
             {'Arqueiro': {'duration': '1:56:30', 'date_completion': 'hoje às 17:02:56 horas', 'quantity': 50}}]
        """

        def parser(url:str) -> dict:

            units = ["Lanceiro", "Espadachim", "Viking", "Arqueiro"  ]

            soup = BeautifulSoup(url, 'html.parser')

            try:
                orders = []
                # find executing order
                timer = soup.find(id = "trainqueue_wrap_barracks")
                timer = list(timer.find_all(attrs = {"class": "lit-item"}))

                queue = soup.find(id = "trainqueue_wrap_barracks").find(class_ = "lit-item").text
                for unit in units:
                    if unit in queue:
                        quantity = [int(s) for s in queue.split() if s.isdigit()][0]
                        orders.append({unit:{"duration": timer[1].text, "date_completion": timer[2].text, "quantity": quantity}})

                # find other orders           
                queue = soup.find(id = "trainqueue_barracks")

                queue = list(queue.find_all(attrs = {"class": "sortable_row"}))
                for element in queue:
                    lista = (list(element.find_all("td")))
                    for unit in units:
                        if unit in element.text:
                            quantity = [int(s) for s in element.text.split() if s.isdigit()][0]
                            orders.append({unit: {"duration": lista[1].text, "date_completion": lista[2].text, "quantity": quantity}})

                return (orders)

            except AttributeError:
                
                return([]) # return empty list if not training any unit

            except Exception: # for unknown exceptions and other exceptions such as unit not being researched or building not built
                # add log
                return([])


        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=barracks&spear=0&sword=0&axe=0&archer=0&_partial"   
            
        with self.session as ses:

                res = ses.get(url).json()["content"]
                return(parser(res)) # error when queue is empty

    def construction_queue(self, village_id: str) -> dict: 

        # TODO: add the time till completion of the queued buildings

        """ returns the queued orders
            return the executing building order and time till completion
            format: {'Est�bulo': '3:21:29'} ['Est�bulo', 'Mercado', 'Mercado', 'Mercado', 'Fazenda']
        """

        def parser(url:str) -> dict:

            """ format: buildings = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=main" 
                returns the executing training queue and the name of the queued buildings 
            """

            buildings_list = ["Mina de Ferro", "Edif�cio principal", "Quartel", "Est�bulo", "Oficina",
                              "Igreja", "Academia", "Ferreiro", "Pra�a de Reuni�es", 
                              "Est�tua", "Mercado", "Bosque", "Po�o de Argila", 
                              "Mina de Ferro", "Fazenda", "Armaz�m", "Muralha"]
    
            soup = BeautifulSoup(url, 'html.parser')

            try:
                buildqueue = soup.find_all(id = "buildqueue") # find building queue
                timer = soup.find("span", class_ = "timer")
                construction_queue = {}
                queue = []
                for element in list(buildqueue):
                    element = element.find_all(class_="lit-item")
                    for ele in element:
                        element = ele.text #building name #.find(class_="order-progress")
                        for count in range(len(buildings_list)):
                            if buildings_list[count] in element:  
                                queue.append(buildings_list[count])
                                if not construction_queue: # make sure you just get the first building                       
                                    construction_queue = {buildings_list[count]: timer.text}

                return(construction_queue, queue)

            except AttributeError:
                
                return ({}) # return empty dict if nothing is being built

            except Exception:
                # add log
                return([]) 
            
        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=main"
            
        with self.session as ses:

                res = ses.get(url).text
                return(parser(res)) # can be improved 

    def merchant_status(self, village_id:str) -> dict: # can be improved

        # TODO: add timers of when new merchants will be available

        """ returns the total number of merchants 
            returns the number of available merchants
            format: {'merchant_available': '83', 'merchant_total': '110'}
        """

        def parser(url:str) -> dict:
            soup = BeautifulSoup(url, 'html.parser')
            merchant_available = soup.find(id = "market_merchant_available_count").text
            merchant_total = soup.find(id = "market_merchant_total_count").text
            return({"merchant_available": merchant_available, "merchant_total": merchant_total})

        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=market&mode=traders"

        with self.session as ses:

                res = ses.get(url).text
                return(parser(res)) # okay

    def smith_info(self, village_id:str) -> dict: # deprecated

        """ {'spear': 'Pesquisado', 'spy': 'Requisitos em falta:', 'ram': 'Requisitos em falta:', 'sword': 'Pesquisado', 'light': 'Requisitos em     falta:', 'catapult': 'Requisitos em falta:', 'axe': 'Pesquisado', 'marcher': 'Requisitos em falta:', 'archer': 'Pesquisado', 'heavy':     'Requisitos em falta:'}
            url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=smith"
        """
        raise NotImplementedError


    def population(self, village_id: str) -> dict:

        def parser(url:str):
            soup = BeautifulSoup(url, 'html.parser')
            pop = soup.find(attrs={"id": "pop_current_label"}).text
            pop_max = soup.find(attrs={"id": "pop_max_label"}).text
            return({"pop": pop, "max_pop": pop_max})

        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={village_id}&screen=overview"

        with self.session as ses:

                res = ses.get(url).text
                return(parser(res)) # okay

#BaseAPI().login("Seelfed", "azulcaneta7", "pt62")
#print(API_get().population("44357"))
#print(API_get().merchant_status("44357"))
#print(API_get().stable_queue("44357"))
#print(API_get().barracks_queue("44357"))
#API_get().number_of_villages("44357")
#print(API_get().garage_queue("44357"))
#print(API_get().construction_queue("44357"))
#print(API_get().attack_power("44357"))
#print(API_get().premium_features("44357"))

"""