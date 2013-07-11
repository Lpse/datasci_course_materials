# Lpse_Code:
from __future__ import print_function
# End of Lpse_Code

import oauth2 as oauth
import urllib2 as urllib


# See Assignment 1 instructions or README for how to get these credentials
access_token_key = "1385502512-HvyikMR9T8hKq7ryll50CRaRaIPr2i8yo2k60kk"
access_token_secret = "vJ99xEXAjLSkxQJxYLDooPzBMHFnBFMyqsWkLdCfm8"

consumer_key = "J4Hi1XVBDcmq4PGhp2ETA"
consumer_secret = "aCMCJ99YKeFdlNTGljqSud8ot2lxAKNXR1VRARQCM"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response


def fetchsamples(lineValue):
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    lineValue+=1
    if(lineValue<21):
      print (line.strip())


if __name__ == '__main__':
  lineValue=int(0)
  fetchsamples(lineValue)
