const BASE_URL = "http://localhost:8000/api/spotify";

export const getSpotifyAuthUrl = async (userId: string) => {
  const response = await fetch(`${BASE_URL}/auth?userId=${userId}`);
  return response.json(); // returns { auth_url: "..." }
};

export const exchangeSpotifyCode = async (code: string) => {
  const response = await fetch(`${BASE_URL}/callback?code=${code}`);
  return response.json(); // access_token, refresh_token, expires_in
};

export const generatePlaylist = async (userId: string, mood: string) => {
  const response = await fetch(`${BASE_URL}/generate-playlist`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId, mood }),
  });
  return response.json();
};

export const createPlaylist = async (userId: string, mood: string) => {
  const response = await fetch(`${BASE_URL}/create-playlist`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId, mood }),
  });
  return response.json(); // playlist URL + track list
};
