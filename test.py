import urllib.robotparser

rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://www.gov.si/robots.txt")
rp.read()
print(rp.can_fetch("*", "https://www.gov.si/"))