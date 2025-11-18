// screens/ResultsScreen.tsx

import React, { useState, useEffect } from "react";
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Alert,
} from "react-native";
import { Linking } from "react-native";

export default function ResultsScreen({ navigation, route }: any) {
  const answers = route?.params?.answers || {};
  const moodResult = route?.params?.moodResult;
  const userId = route?.params?.userId;

  // Spotify Token passed from SpotifySuccessScreen
  const spotifyAccessToken = route?.params?.spotifyAccessToken || null;

  // Real playlist songs from backend
  const [songs, setSongs] = useState<any[]>([]);
  const [loadingSongs, setLoadingSongs] = useState(false);
  const [playlistUrl, setPlaylistUrl] = useState<string | null>(null);

  // Store the mood locally so it persists across navigation
  const [storedMood, setStoredMood] = useState<string | null>(null);

  // Set mood when component receives it
  useEffect(() => {
    if (moodResult?.dominantMood) {
      setStoredMood(moodResult.dominantMood);
      console.log("Stored mood:", moodResult.dominantMood);
    }
  }, [moodResult]);

  const dominantMood = storedMood || moodResult?.dominantMood || "energetic";

  console.log("RESULTS SCREEN - Mood:", dominantMood, "Token:", spotifyAccessToken);

  // -------------------------------------------------------------
  // IF TOKEN EXISTS → FETCH REAL SONGS FROM BACKEND
  // -------------------------------------------------------------
  useEffect(() => {
    if (!spotifyAccessToken) {
      console.log("No Spotify token yet.");
      return;
    }

    console.log("Fetching real playlist...");
    fetchRealSpotifyPlaylist();
  }, [spotifyAccessToken]);

  // -------------------------------------------------------------
  // Create Playlist on Spotify
  // -------------------------------------------------------------
  const fetchRealSpotifyPlaylist = async () => {
    try {
      setLoadingSongs(true);

      const response = await fetch(
        "http://localhost:8000/api/spotify/create-playlist",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            accessToken: spotifyAccessToken,
            mood: dominantMood,
            userId: userId || "guest",
          }),
        }
      );

      const data = await response.json();

      if (!data.success) {
        Alert.alert("Error", "Failed to create playlist on Spotify.");
        setLoadingSongs(false);
        return;
      }

      console.log("PLAYLIST CREATED:", data);
      console.log("Spotify URL:", data.playlistUrl);

      // Set the tracks for display
      setPlaylistUrl(data.playlistUrl);
      setSongs(data.tracks || []);

      Alert.alert(
        "Success! 🎉",
        `Playlist "${data.playlistName}" created with ${data.tracksAdded} tracks!\n\nCheck your Spotify app to listen.`,
        [
          {
            text: "Open in Spotify",
            onPress: () => Linking.openURL(data.playlistUrl),
          },
          { text: "OK" },
        ]
      );
    } catch (err) {
      console.log("Playlist creation error:", err);
      Alert.alert("Error", "Failed to create Spotify playlist.");
    } finally {
      setLoadingSongs(false);
    }
  };

  // -------------------------------------------------------------
  // 3️⃣ Spotify Login Handler
  // -------------------------------------------------------------
  const handleSpotifyLogin = async () => {
    try {
      console.log("Starting Spotify auth with mood:", dominantMood);

      // Pass mood to backend so it can be retrieved after auth
      const res = await fetch(
        `http://localhost:8000/api/spotify/auth?userId=${userId}&mood=${dominantMood}`
      );
      const data = await res.json();

      if (data.authUrl) {
        Linking.openURL(data.authUrl);
      } else {
        Alert.alert("Error", "No Spotify authorization URL returned.");
      }
    } catch (error) {
      console.log("Spotify login error:", error);
      Alert.alert("Error", "Failed to start Spotify authentication.");
    }
  };

  const handleCreateNewPlaylist = () => navigation.navigate("Onboarding");

  const getMoodEmoji = (mood: string) => {
    const moodEmojis: any = {
      energetic: "⚡",
      calm: "🌊",
      introspective: "🌙",
      adventurous: "🗺️",
    };
    return moodEmojis[mood] || "🎵";
  };

  const getMoodColor = (mood: string) => {
    const moodColors: any = {
      energetic: "#FF6B6B",
      calm: "#4ECDC4",
      introspective: "#A569BD",
      adventurous: "#F39C12",
    };
    return moodColors[mood] || "#3BF664";
  };

  return (
    <View style={styles.container}>
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <View
            style={[
              styles.resultIcon,
              { backgroundColor: getMoodColor(dominantMood) },
            ]}
          >
            <Text style={styles.resultIconText}>
              {getMoodEmoji(dominantMood)}
            </Text>
          </View>

          <Text style={styles.title}>
            Your {dominantMood.charAt(0).toUpperCase() + dominantMood.slice(1)}{" "}
            Vibe
          </Text>

          <Text style={styles.subtitle}>
            Based on your quiz, we curated these tracks just for you.
          </Text>
        </View>

        {/* Playlist Section */}
        <View style={styles.playlistCard}>
          <View style={styles.playlistHeader}>
            <View
              style={[
                styles.playlistCover,
                { backgroundColor: getMoodColor(dominantMood) },
              ]}
            >
              <Text style={styles.playlistCoverIcon}>
                {getMoodEmoji(dominantMood)}
              </Text>
            </View>

            <View style={styles.playlistInfo}>
              <Text style={styles.playlistName}>Your {dominantMood} Mix</Text>
              <Text style={styles.playlistDetails}>
                {songs.length > 0 ? songs.length : 10} songs • Personalized
              </Text>
            </View>
          </View>
        </View>

        {/* Tracks Section */}
        <View style={styles.songsSection}>
          <Text style={styles.sectionTitle}>Tracks</Text>

          {/* Loading Spinner */}
          {loadingSongs && (
            <Text style={{ textAlign: "center", paddingVertical: 20 }}>
              Loading Spotify songs...
            </Text>
          )}

          {/* Show REAL SONGS */}
          {!loadingSongs &&
            songs.length > 0 &&
            songs.map((track: any, index: number) => (
              <View key={index} style={styles.songItem}>
                <View style={styles.songLeft}>
                  <Text style={styles.songNumber}>{index + 1}</Text>

                  <View style={styles.songInfo}>
                    <Text style={styles.songTitle}>{track.name}</Text>
                    <Text style={styles.songArtist}>
                      {track.artists?.join(", ")}
                    </Text>
                  </View>
                </View>

                <Text style={styles.songDuration}>
                  {track.duration || "3:30"}
                </Text>
              </View>
            ))}

          {/* If no Spotify: show placeholder */}
          {!spotifyAccessToken && songs.length === 0 && (
            <Text style={{ textAlign: "center", marginTop: 20 }}>
              Connect Spotify to load your playlist.
            </Text>
          )}
        </View>
      </ScrollView>

      {/* Footer */}
      <View style={styles.footer}>
        <TouchableOpacity
          style={styles.createButton}
          onPress={handleSpotifyLogin}
        >
          <Text style={styles.createButtonText}>🎧 Connect Spotify</Text>
        </TouchableOpacity>

        <View style={styles.actionButtons}>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={handleCreateNewPlaylist}
          >
            <Text style={styles.actionButtonText}>🔄 New Playlist</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.actionButton}>
            <Text style={styles.actionButtonText}>👤 Profile</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

// ---------- STYLES ----------
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#FFFFFF" },
  content: { flex: 1 },
  header: { alignItems: "center", padding: 24, paddingTop: 60 },
  resultIcon: {
    width: 80,
    height: 80,
    borderRadius: 40,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 16,
  },
  resultIconText: { fontSize: 40 },
  title: {
    fontSize: 32,
    fontWeight: "bold",
    textAlign: "center",
    color: "#1F2937",
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    textAlign: "center",
    color: "#6B7280",
    paddingHorizontal: 32,
  },
  playlistCard: {
    margin: 24,
    padding: 16,
    borderRadius: 16,
    backgroundColor: "#F9FAFB",
    borderWidth: 1,
    borderColor: "#E5E7EB",
  },
  playlistHeader: {
    flexDirection: "row",
    gap: 16,
    alignItems: "center",
  },
  playlistCover: {
    width: 80,
    height: 80,
    borderRadius: 8,
    alignItems: "center",
    justifyContent: "center",
  },
  playlistCoverIcon: { fontSize: 40 },
  playlistInfo: { flex: 1 },
  playlistName: { fontSize: 18, fontWeight: "600" },
  playlistDetails: { color: "#6B7280", fontSize: 12 },
  songsSection: { padding: 24 },
  sectionTitle: { fontSize: 18, fontWeight: "600", marginBottom: 16 },
  songItem: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#E5E7EB",
  },
  songLeft: { flexDirection: "row", gap: 16, flex: 1, alignItems: "center" },
  songNumber: { width: 24, color: "#9CA3AF" },
  songInfo: { flex: 1 },
  songTitle: { fontSize: 14, fontWeight: "600" },
  songArtist: { fontSize: 12, color: "#6B7280" },
  songDuration: { color: "#9CA3AF", fontSize: 12 },
  footer: { padding: 24, backgroundColor: "#FFFFFF" },
  createButton: {
    backgroundColor: "#3BF664",
    padding: 16,
    borderRadius: 12,
    alignItems: "center",
    marginBottom: 12,
  },
  createButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
  actionButtons: { flexDirection: "row", gap: 12 },
  actionButton: {
    flex: 1,
    backgroundColor: "#F9FAFB",
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#E5E7EB",
    alignItems: "center",
  },
  actionButtonText: {
    fontSize: 14,
    fontWeight: "600",
    color: "#374151",
  },
});
