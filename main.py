import requests, json, sys, time, os
import spotify_lyrics_scraper as sls

authorizedURL = 'https://discord.com/api/v8/users/@me/settings'
githubCheckURL = 'https://raw.githubusercontent.com/ITemply/discord-Lyrics/main/authorize.json'

authoredVersion = '0.01'

def trackIdStripper(songURL):
    split1 = songURL.split('track/')
    split2 = split1[1].split('?si')
    return split2[0]
    
def scrapeLyrics(songID, spotToken):
    lyricsJson = sls.getLyrics(spotToken, trackId=songID)
    officalLyrics = lyricsJson['message']['lyrics']['lines']
    
    lyricsList = []

    for line in officalLyrics:
        lyricsList.append(line['words'])

    return lyricsList

def versionCheck(version):
    githubSeek = requests.get(url=githubCheckURL)
    jsonData = json.loads(json.dumps(githubSeek.json()))

    authorizedVersion = jsonData['Version']

    if authorizedVersion == version:
        return True
    else:
        return False

def getMessageType(messageType):
    githubSeek = requests.get(url=githubCheckURL)
    jsonData = json.loads(json.dumps(githubSeek.json()))

    validMessage = jsonData['ValidMessage']
    invalidMessage = jsonData['InvalidMessage']

    if messageType == 1:
        return validMessage
    elif messageType == 2:
        return invalidMessage
    else:
        return 'Invalid Message Type'

def statusChange(statusMessage, token, url, statusType):
    header = {
        'authorization': token
    }

    jsonData = {
        'status': statusType,
        'custom_status': {
            'text': statusMessage
        }
    }

    request = requests.patch(url, headers=header, json=jsonData)

    return request

def selectStatusType(status):
    if status == 1:
        return 'online'
    elif status == 2:
        return 'idle'
    elif status == 3:
        return 'dnd'
    elif status == 4:
        return 'invisible'

if __name__ == '__main__':
    os.system('cls||clear')

    if versionCheck(authoredVersion):
        print(getMessageType(1))
        print('Starting...')
    else:
        sys.exit(getMessageType(2))

    time.sleep(2)

    os.system('cls||clear')

    discordToken = input('Discord Status Lyrics\n\nDiscord Token > ')
    os.system('cls||clear')
    spotifyToken = input('Discord Status Lyrics\n\nSpotify Token > ')
    spotToken = sls.getToken(spotifyToken)
    os.system('cls||clear')

    while True:
        os.system('cls||clear')
        timeBetween = int(input('Discord Status Lyrics\n\nTime Between Lyric > '))
        os.system('cls||clear')
        spotifySongURL = input('Discord Status Lyrics\n\nSpotify Song URL > ')
        os.system('cls||clear')
        statusType = input('Discord Status Lyrics\n\n1 = Online\n2 = Idle\n3 = DND\n4 = Invisble\n\nDiscord Status Type > ')
        os.system('cls||clear')

        if timeBetween > 10:
            timeBetween = 10
        elif timeBetween < 1:
            timeBetween = 1

        trackId = trackIdStripper(spotifySongURL)
        lyrics = scrapeLyrics(trackId, spotToken)

        for line in lyrics:
            os.system('cls||clear')
            print('Discord Status Lyrics\n\nSending Lyric: ' + line + '\n\nPress Ctrl+C to quit.')
            statusChange(line, discordToken, authorizedURL, selectStatusType(statusType))
            time.sleep(timeBetween)
