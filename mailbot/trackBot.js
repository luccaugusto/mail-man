export class TrackBot {
  constructor(trackID) {
    this.trackID = trackID;
    this.cookies = [];
    this.headers = {
      "Host": "rastreamento.correios.com.br",
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      "Accept-Encoding": "gzip, deflate, br",
      "Accept-Language": "en-US,en;q=0.5",
      "Referer":	"https://rastreamento.correios.com.br/app/index.php",
      "DNT": 1,
      "Connection": "keep-alive",
      "Upgrade-Insecure-Requests": 1,
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "none",
      "Sec-Fetch-User": "?1",
    }
  }
}


