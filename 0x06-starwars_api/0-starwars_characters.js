#!/usr/bin/node
const request = require('request');
const API_URL = 'https://swapi-api.hbtn.io/api';

if (process.argv.length > 2) {
  const movieId = process.argv[2];
  request(`${API_URL}/films/${movieId}/`, (err, _, body) => {
    if (err) {
      console.error(err);
      process.exit(1);
    }

    let charactersURL;
    try {
      charactersURL = JSON.parse(body).characters;
    } catch (parseErr) {
      console.error('Error parsing JSON:', parseErr);
      process.exit(1);
    }

    // Use map to create promises to fetch each character name
    const characterNames = charactersURL.map(
      url => new Promise((resolve, reject) => {
        request(url, (promiseErr, __, charactersReqBody) => {
          if (promiseErr) {
            reject(promiseErr);
            return;
          }
          try {
            const characterName = JSON.parse(charactersReqBody).name;
            resolve(characterName);
          } catch (parseCharErr) {
            reject(parseCharErr);
          }
        });
      })
    );

    // Resolve all character name promises
    Promise.all(characterNames)
      .then(names => console.log(names.join('\n')))
      .catch(allErr => console.error('Error fetching character names:', allErr));
  });
} else {
  console.error('Please provide a movie ID as an argument');
  process.exit(1);
}
