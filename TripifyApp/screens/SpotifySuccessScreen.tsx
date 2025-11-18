import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, ActivityIndicator } from "react-native";
import * as WebBrowser from "expo-web-browser";
import { useNavigation } from "@react-navigation/native";

export default function SpotifySuccessScreen() {
  const navigation = useNavigation();

  const extractDataFromUrl = () => {
    const url = window.location.href;
    const params = new URLSearchParams(url.split("?")[1]);

    return {
      accessToken: params.get("access_token"),
      refreshToken: params.get("refresh_token"),
      mood: params.get("mood"),
      userId: params.get("userId"),
    };
  };

  useEffect(() => {
    const { accessToken, refreshToken, mood, userId } = extractDataFromUrl();

    console.log("Spotify callback data:", { accessToken: !!accessToken, mood, userId });

    if (accessToken) {
      // Navigate back to Results with all data from backend
      navigation.navigate("Results", {
        spotifyAccessToken: accessToken,
        spotifyRefreshToken: refreshToken,
        moodResult: { dominantMood: mood || 'energetic' },
        userId: userId || 'guest',
      });
    }
  }, []);

  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#1DB954" />
      <Text style={styles.text}>Connecting to Spotify...</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  text: {
    marginTop: 20,
    fontSize: 18,
    color: "#1DB954",
  },
});
