import axios from 'axios';
import fs from 'fs';
import { cookiesToString } from './utils.js';

export async function getSessionCookies(headers) {
  let resp = await axios.get(
    'https://rastreamento.correios.com.br/app/index.php',
    {
      headers: {
        ...headers,
      }
    }
  );
  return resp.headers['set-cookie'];
}

export async function getSecureImage(headers, cookies, filename = 'captcha.png') {
  const response = await axios.get(
    'https://rastreamento.correios.com.br/core/securimage/securimage_show.php',
    {
      responseType: "arraybuffer",
      headers: {
        ...headers,
        Accept: 'image/avif,image/webp,*/*',
        cookie: cookiesToString(cookies),
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
      }
    }
  );
  const base64Image = btoa(
    new Uint8Array(response.data).reduce(
      (data, byte) => data + String.fromCharCode(byte),
      ''
    )
  );
  fs.writeFile(filename, new Buffer.from(base64Image, 'base64') , (err) => {if (err) console.log(err)});
  return {captchaCookie: response.headers['set-cookie'][0], captchaImage: base64Image};
}

export async function getControle(trackBot) {
  const response = await axios.get(
    'https://rastreamento.correios.com.br/app/controle.php',
    {
      headers: {
        ...trackBot.headers,
        "Accept":	"*/*",
        "Cookie":	cookiesToString(trackBot.cookies),
        "Sec-Fetch-Dest":	"empty",
        "Sec-Fetch-Mode":	"cors",
        "Sec-Fetch-Site":	"same-origin",
      }
    }
  )
  console.log(response.data);
}

export async function getResult(headers, cookies, captchaAnswer, trackID) {
  return axios.get(
    `https://rastreamento.correios.com.br/app/resultado.php?objeto=${trackID}&captcha=${captchaAnswer}&mqs=S`,
    {
      headers: {
        ...headers,
        Accept: '*/*',
        Cookie: cookiesToString(cookies),
        "Sec-Fetch-Dest":	"empty",
        "Sec-Fetch-Mode":	"cors",
        "Sec-Fetch-Site":	"same-origin",
      },
    }
  );
}
