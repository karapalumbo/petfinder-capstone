const BASE_URL = "https://api.petfinder.com/v2/animals";

async function getPets() {
  let res = await axios.get(BASE_URL);
  console.log(res);
  return res.data;
}

getPets();
