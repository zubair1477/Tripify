// screens/ResultsScreen.tsx
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Alert,
} from "react-native";
import { Linking } from "react-native"; // <-- required for opening URLs

const playlistSongs = [
  {
    id: 1,
    title: "Placeholder Song 1",
    artist: "Placeholder Artist",
    duration: "3:45",
  },
  {
    id: 2,
    title: "Placeholder Song 2",
    artist: "Placeholder Artist",
    duration: "4:12",
  },
  {
    id: 3,
    title: "Placeholder Song 3",
    artist: "Placeholder Artist",
    duration: "3:28",
  },
  {
    id: 4,
    title: "Placeholder Song 4",
    artist: "Placeholder Artist",
    duration: "4:01",
  },
  {
    id: 5,
    title: "Placeholder Song 5",
    artist: "Placeholder Artist",
    duration: "3:56",
  },
  {
    id: 6,
    title: "Placeholder Song 6",
    artist: "Placeholder Artist",
    duration: "4:23",
  },
  {
    id: 7,
    title: "Placeholder Song 7",
    artist: "Placeholder Artist",
    duration: "3:34",
  },
  {
    id: 8,
    title: "Placeholder Song 8",
    artist: "Placeholder Artist",
    duration: "4:18",
  },
  {
    id: 9,
    title: "Placeholder Song 9",
    artist: "Placeholder Artist",
    duration: "3:52",
  },
  {
    id: 10,
    title: "Placeholder Song 10",
    artist: "Placeholder Artist",
    duration: "4:05",
  },
];

export default function ResultsScreen({ navigation, route }: any) {
  const answers = route?.params?.answers || {};
  const moodResult = route?.params?.moodResult;
  const userId = route?.params?.userId;

  const getMoodEmoji = (mood: string) => {
    const moodEmojis: { [key: string]: string } = {
      energetic: "⚡",
      calm: "🌊",
      introspective: "🌙",
      adventurous: "🗺️",
    };
    return moodEmojis[mood.toLowerCase()] || "🎵";
  };

  const getMoodColor = (mood: string) => {
    const moodColors: { [key: string]: string } = {
      energetic: "#FF6B6B",
      calm: "#4ECDC4",
      introspective: "#A569BD",
      adventurous: "#F39C12",
    };
    return moodColors[mood.toLowerCase()] || "#3BF664";
  };

  /***
   * SPOTIFY LOGIN HANDLER
   * Calls backend → gets Spotify auth URL → opens login screen
   */
  const handleSpotifyLogin = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/api/spotify/auth?userId=${userId}`
      );
      const data = await res.json();

      if (data.authUrl) {
        Linking.openURL(data.authUrl);
      } else {
        Alert.alert("Error", "No Spotify authorization URL was returned.");
      }
    } catch (error) {
      console.log("Spotify login error:", error);
      Alert.alert("Error", "Failed to start Spotify authentication.");
    }
  };

  const handleCreateNewPlaylist = () => {
    navigation.navigate("Onboarding");
  };

  const handleGoToProfile = () => {
    console.log("Navigate to profile (to be created)");
  };

  const dominantMood = moodResult?.dominantMood || "energetic";
  const moodScores = moodResult?.moodScores;

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
            Based on your quiz results, we have curated these tracks just for
            you
          </Text>
        </View>

        {/* Mood Scores */}
        {moodScores && (
          <View style={styles.moodScoresCard}>
            <Text style={styles.moodScoresTitle}>Your Mood Breakdown</Text>

            {Object.entries(moodScores).map(([mood, score]) => {
              const scoreValue = typeof score === "number" ? score : 0;

              return (
                <View key={mood} style={styles.moodScoreRow}>
                  <View style={styles.moodScoreLabel}>
                    <Text style={styles.moodScoreEmoji}>
                      {getMoodEmoji(mood)}
                    </Text>
                    <Text style={styles.moodScoreName}>
                      {mood.charAt(0).toUpperCase() + mood.slice(1)}
                    </Text>
                  </View>

                  <View style={styles.moodScoreBar}>
                    <View
                      style={[
                        styles.moodScoreFill,
                        {
                          width: `${scoreValue}%`,
                          backgroundColor: getMoodColor(mood),
                        },
                      ]}
                    />
                  </View>

                  <Text style={styles.moodScoreValue}>
                    {scoreValue.toFixed(0)}%
                  </Text>
                </View>
              );
            })}
          </View>
        )}

        {/* Playlist Card */}
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
              <Text style={styles.playlistName}>
                Your{" "}
                {dominantMood.charAt(0).toUpperCase() + dominantMood.slice(1)}{" "}
                Mix
              </Text>
              <Text style={styles.playlistDetails}>
                {playlistSongs.length} songs • Personalized for you
              </Text>
            </View>

            <TouchableOpacity
              style={[
                styles.playButton,
                { backgroundColor: getMoodColor(dominantMood) },
              ]}
            >
              <View style={styles.playTriangle} />
            </TouchableOpacity>
          </View>
        </View>

        {/* Song List */}
        <View style={styles.songsSection}>
          <Text style={styles.sectionTitle}>Tracks</Text>

          {playlistSongs.map((song, index) => (
            <View key={song.id} style={styles.songItem}>
              <View style={styles.songLeft}>
                <Text style={styles.songNumber}>{index + 1}</Text>

                <View style={styles.songInfo}>
                  <Text style={styles.songTitle}>{song.title}</Text>
                  <Text style={styles.songArtist}>{song.artist}</Text>
                </View>
              </View>

              <Text style={styles.songDuration}>{song.duration}</Text>
            </View>
          ))}
        </View>
      </ScrollView>

      {/* Footer */}
      <View style={styles.footer}>
        {/* CONNECT SPOTIFY BUTTON */}
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

          <TouchableOpacity
            style={styles.actionButton}
            onPress={handleGoToProfile}
          >
            <Text style={styles.actionButtonText}>👤 Profile</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

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
  moodScoresCard: {
    margin: 24,
    padding: 20,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#E5E7EB",
  },
  moodScoresTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 16,
  },
  moodScoreRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 12,
    gap: 8,
  },
  moodScoreLabel: {
    flexDirection: "row",
    alignItems: "center",
    width: 140,
    gap: 8,
  },
  moodScoreEmoji: { fontSize: 20 },
  moodScoreName: { fontSize: 14, fontWeight: "500" },
  moodScoreBar: {
    flex: 1,
    height: 8,
    backgroundColor: "#E5E7EB",
    borderRadius: 4,
    overflow: "hidden",
  },
  moodScoreFill: {
    height: "100%",
    borderRadius: 4,
  },
  moodScoreValue: {
    width: 45,
    textAlign: "right",
    fontSize: 14,
    fontWeight: "600",
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
  playButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: "center",
    justifyContent: "center",
  },
  playTriangle: {
    width: 0,
    height: 0,
    marginLeft: 4,
    borderLeftWidth: 14,
    borderTopWidth: 10,
    borderBottomWidth: 10,
    borderLeftColor: "#FFFFFF",
    borderTopColor: "transparent",
    borderBottomColor: "transparent",
  },
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
