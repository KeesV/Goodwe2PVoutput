import requests
import goodweData
import iGoodwe

class readGoodwe( iGoodwe.iGoodwe) :

   #--------------------------------------------------------------------------
   def __init__(self, url, login_url, station_id):
   # Goodwe-power reading class. Reads the Goodwe-power.com website
   # from the specified URL and station ID.
   #
      self.m_query = "&InventerType=GridInventer&HaveAdverseCurrentData=0&HaveEnvironmentData=0"
      self.m_goodwe_url = url
      self.m_login_url = login_url
      self.m_station_id = station_id
      self.m_session = None
      self.m_gwData = None
      

   #--------------------------------------------------------------------------
   def login(self, username, password):
   # Log in Goodwe-power web site.
   #
      payload = {
         'username': username,
	 'password': password }
	 
      with requests.Session() as self.m_session:
         p = self.m_session.post( self.m_login_url, data=payload)
	 if p.status_code != 200:
	    if 'incorrect' in p.text:
	       print "Incorrect password for user " + str(username)
               raise IOError
	    else:
	       print "Cannot Log in " + str(self.m_login_url)
               raise IOError
	 else:
	    print "User " + str(username) + " Logged in"
	 

    #--------------------------------------------------------------------------
   def is_online( self):
   #TRUE when the GoodWe inverter returns the correct status
   #
      return True

   #--------------------------------------------------------------------------
   def read_sample_data( self):
   # Read the data. When a failure is found, it is tried upto 3 times. After 
   # that, an error is logged.
   #
      url = self.m_goodwe_url + "?ID=" + self.m_station_id + self.m_query
      tries = 0
      
      while True:
         try:
            sample = self._read_data( url)
            self.m_gwData = goodweData.goodweData( sample)
	    return self.m_gwData.get_sample()
         except:
            tries += 1
            if tries > 3:
               print "Cannot read data after " + str(tries) + " tries."
               raise ValueError

         
      
   #--------------------------------------------------------------------------
   def _read_data( self, url):
   # Do the actual read from the URL
   #
      if self.m_session:
         print "Reading from URL: " + url
         # url = "http://goodwe-power.com/PowerStationPlatform/PowerStationReport/InventerDetail?ID=7cb8d7d1-166d-47ca-871b-601e1f6b7575&InventerType=GridInventer&HaveAdverseCurrentData=0&HaveEnvironmentData=0"
         r = self.m_session.get( url, timeout=180)
      return r.content
                  
#---------------- End of file ------------------------------------------------
