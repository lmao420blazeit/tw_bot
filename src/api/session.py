from client import client
import time
import logging
from tw_log import action_log
from api_exceptions import SessionException

class Session:

    """
    base api class, contains login/logout functions, 
    requests and passes session to other classes

    creates new session
    """

    _instance = None

    _status_code = {"200": "OK", 
                    "202": "Created",
                    "204": "Accepted", 
                    "400": "Bad Request", 
                    "500": "Internal Server Error"}

    HEADERS = {"Content-Type": "application/x-www-form-urlencoded",
                   "X-Requested-With": "XMLHttpRequest",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Firefox/64.0"}
    

    def __new__(self, username:str, password:str, gameworld: str):
        
        
        self.gameworld = gameworld
        self.username = username
        self.password = password

        self.session = client().session
        self.csrf_token = None
        self.session_id = None
        self.time = time.time()

        if not self._instance:
           self._instance = super(Session, self).__new__(self)
           
        return(self._instance )

    def get_session(self):

        """Returns existing session."""

        return(self.session)

    def verify_session(self):

        """Indicates if session exists.
            :True: valid session
            :False: rotten session"""       

        try:
            url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={self.village_id}&screen=overview"
            with self.session as ses:
             
                res = ses.get(url)
                if res.url == "https://www.tribalwars.com.pt/?session_expired=1":
                    return(False)
                else:
                    return(True)

        except AttributeError:

            self.new_session()
            return(True)

    def new_session(self) -> None:

        self.session.headers = Session.HEADERS

        with self.session as ses:

            # get page cookies
            url = "https://www.tribalwars.com.pt"
            res = ses.get(url)
            
            # authentification
            authurl = "https://www.tribalwars.com.pt/page/auth"
            data = f"username={self.username}&password={self.password}&remember=1"


            try:

                res = self.session.post(authurl, data=data, allow_redirects = False)

                if res.json()["status"] == "success":

                    # retrieve login token
                    url_gameworld = f"https://www.tribalwars.com.pt/page/play/{self.gameworld}"
                    res = ses.get(url_gameworld, allow_redirects=False)
                    url_token = res.json()["uri"] # returns redirect link
  
                    # get global village cookie
                    res = ses.get(url_token)
                    self.village_id = res.cookies.get_dict().get("global_village_id")
                    self.session_id = self.session.cookies.get_dict().get("sid").strip("%")

                    self.session.headers['TribalWars-Ajax'] = '1'

                    # logged in
                    url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={self.village_id}&screen=api&ajax=resources_schedule&id={self.village_id}&client_time={self.time}"
                    res = ses.get(url)

                    # get csrf_token token
                    self.csrf_token = res.json()['game_data']['csrf']

                    # check if login was successful
                    if res.status_code == 200 and self.csrf_token != None and self.session_id != None:
                        action_log("Login successful!")
                        return (self.session)

                    else:
                        action_log("Login unsuccessful")

            except Exception as e:
                
                action_log("Wrong username & password combination") # done
                logging.error(e)


    def logout(self) -> None:
        
        url = f"https://{self.gameworld}.tribalwars.com.pt/game.php?village={self.village_id}&screen=&action=logout&h={self.csrf_token}"

        with self.session as ses:

            res = ses.get(url)

        if res.status_code == 200:
            action_log("Logout successful!") 

        else:
            action_log("Logout unsuccessful, probably already logged out")
