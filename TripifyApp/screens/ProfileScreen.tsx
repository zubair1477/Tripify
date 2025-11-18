// screens/ProfileScreen.tsx
 
import React, { useState, useEffect } from "react";
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
  Linking,
} from "react-native";
 
interface Playlist {
  id: string;
  mood: string;
  playlistName: string;
  playlistUrl: string;
  tracksCount: number;
  createdAt: string;
}
 
export default function ProfileScreen({ navigation, route }: any) {
  const userId = route?.params?.userId || "guest";
  const userName = route?.params?.userName || "User";
 
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  const [loading, setLoading] = useState(true);
 
  useEffect(() => {
    fetchUserPlaylists();
  }, []);
 
  const fetchUserPlaylists = async () => {
    try {
      setLoading(true);
 
      const response = await fetch(
        `http://localhost:8000/api/spotify/playlists/${userId}`
      );
 
      const data = await response.json();
 
      if (data.playlists) {
        setPlaylists(data.playlists);
      }
    } catch (error) {
      console.error("Error fetching playlists:", error);
      Alert.alert("Error", "Failed to load your playlists.");
    } finally {
      setLoading(false);
    }
  };
 
  const getMoodEmoji = (mood: string) => {
    const moodEmojis: any = {
      energetic: "⚡",
      calm: "🌊",
      introspective: "🌙",
      adventurous: "🗺️",
    };
    return moodEmojis[mood.toLowerCase()] || "🎵";
  };
 
  const getMoodColor = (mood: string) => {
    const moodColors: any = {
      energetic: "#FF6B6B",
      calm: "#4ECDC4",
      introspective: "#A569BD",
      adventurous: "#F39C12",
    };
    return moodColors[mood.toLowerCase()] || "#3BF664";
  };
 
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
 
    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
    return date.toLocaleDateString();
  };
 
  const handlePlaylistPress = (playlistUrl: string) => {
    Linking.openURL(playlistUrl);
  };
 
  const handleCreateNewPlaylist = () => {
    navigation.navigate("Onboarding", { userId, userName });
  };
 
  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerTop}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Text style={styles.backButtonText}>← Back</Text>
          </TouchableOpacity>
        </View>
 
        <View style={styles.profileSection}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>
              {userName.charAt(0).toUpperCase()}
            </Text>
          </View>
          <Text style={styles.userName}>{userName}</Text>
          <Text style={styles.userSubtitle}>
            {playlists.length} {playlists.length === 1 ? "playlist" : "playlists"} created
          </Text>
        </View>
      </View>
 
      {/* Playlists List */}
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.playlistsSection}>
          <Text style={styles.sectionTitle}>Your Playlists</Text>
 
          {loading ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#3BF664" />
              <Text style={styles.loadingText}>Loading your playlists...</Text>
            </View>
          ) : playlists.length === 0 ? (
            <View style={styles.emptyState}>
              <Text style={styles.emptyEmoji}>🎵</Text>
              <Text style={styles.emptyTitle}>No playlists yet</Text>
              <Text style={styles.emptySubtitle}>
                Take the mood quiz to create your first personalized playlist!
              </Text>
              <TouchableOpacity
                style={styles.createButton}
                onPress={handleCreateNewPlaylist}
              >
                <Text style={styles.createButtonText}>
                  Create Your First Playlist
                </Text>
              </TouchableOpacity>
            </View>
          ) : (
            playlists.map((playlist) => (
              <TouchableOpacity
                key={playlist.id}
                style={styles.playlistCard}
                onPress={() => handlePlaylistPress(playlist.playlistUrl)}
              >
                <View
                  style={[
                    styles.playlistIcon,
                    { backgroundColor: getMoodColor(playlist.mood) },
                  ]}
                >
                  <Text style={styles.playlistIconEmoji}>
                    {getMoodEmoji(playlist.mood)}
                  </Text>
                </View>
 
                <View style={styles.playlistInfo}>
                  <Text style={styles.playlistName}>
                    {playlist.playlistName}
                  </Text>
                  <Text style={styles.playlistMood}>
                    {playlist.mood.charAt(0).toUpperCase() +
                      playlist.mood.slice(1)}{" "}
                    • {playlist.tracksCount} songs
                  </Text>
                  <Text style={styles.playlistDate}>
                    {formatDate(playlist.createdAt)}
                  </Text>
                </View>
 
                <Text style={styles.playlistArrow}>→</Text>
              </TouchableOpacity>
            ))
          )}
        </View>
      </ScrollView>
 
      {/* Footer */}
      {!loading && playlists.length > 0 && (
        <View style={styles.footer}>
          <TouchableOpacity
            style={styles.newPlaylistButton}
            onPress={handleCreateNewPlaylist}
          >
            <Text style={styles.newPlaylistButtonText}>
              + Create New Playlist
            </Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
}
 
// ---------- STYLES ----------
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
  },
  header: {
    backgroundColor: "#F9FAFB",
    paddingTop: 60,
    paddingBottom: 24,
    borderBottomWidth: 1,
    borderBottomColor: "#E5E7EB",
  },
  headerTop: {
    paddingHorizontal: 24,
    marginBottom: 16,
  },
  backButton: {
    alignSelf: "flex-start",
  },
  backButtonText: {
    fontSize: 16,
    color: "#3BF664",
    fontWeight: "600",
  },
  profileSection: {
    alignItems: "center",
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: "#3BF664",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 12,
  },
  avatarText: {
    fontSize: 36,
    fontWeight: "bold",
    color: "#FFFFFF",
  },
  userName: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#1F2937",
    marginBottom: 4,
  },
  userSubtitle: {
    fontSize: 14,
    color: "#6B7280",
  },
  content: {
    flex: 1,
  },
  playlistsSection: {
    padding: 24,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#1F2937",
    marginBottom: 16,
  },
  loadingContainer: {
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 60,
  },
  loadingText: {
    marginTop: 12,
    fontSize: 14,
    color: "#6B7280",
  },
  emptyState: {
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 60,
    paddingHorizontal: 32,
  },
  emptyEmoji: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#1F2937",
    marginBottom: 8,
  },
  emptySubtitle: {
    fontSize: 14,
    color: "#6B7280",
    textAlign: "center",
    marginBottom: 24,
  },
  createButton: {
    backgroundColor: "#3BF664",
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 12,
  },
  createButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
  playlistCard: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#F9FAFB",
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: "#E5E7EB",
  },
  playlistIcon: {
    width: 60,
    height: 60,
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 16,
  },
  playlistIconEmoji: {
    fontSize: 28,
  },
  playlistInfo: {
    flex: 1,
  },
  playlistName: {
    fontSize: 16,
    fontWeight: "600",
    color: "#1F2937",
    marginBottom: 4,
  },
  playlistMood: {
    fontSize: 13,
    color: "#6B7280",
    marginBottom: 2,
  },
  playlistDate: {
    fontSize: 12,
    color: "#9CA3AF",
  },
  playlistArrow: {
    fontSize: 20,
    color: "#9CA3AF",
    marginLeft: 8,
  },
  footer: {
    padding: 24,
    backgroundColor: "#FFFFFF",
    borderTopWidth: 1,
    borderTopColor: "#E5E7EB",
  },
  newPlaylistButton: {
    backgroundColor: "#3BF664",
    padding: 16,
    borderRadius: 12,
    alignItems: "center",
  },
  newPlaylistButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
});