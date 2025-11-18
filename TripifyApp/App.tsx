import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import * as Linking from "expo-linking";
 
import LoginScreen from "./screens/LoginScreen";
import SignupScreen from "./screens/SignupScreen";
import onboarding from "./screens/onboarding";
import QuizScreen from "./screens/QuizScreen";
import ResultsScreen from "./screens/ResultsScreen";
import SpotifySuccessScreen from "./screens/SpotifySuccessScreen";
import ProfileScreen from "./screens/ProfileScreen";
 
const Stack = createNativeStackNavigator();
 
// 🔥 Deep Linking Config
const linking = {
  prefixes: ["http://localhost:8081"],
  config: {
    screens: {
      Login: "login",
      Signup: "signup",
      Onboarding: "onboarding",
      Quiz: "quiz",
      Results: "results",
      SpotifySuccess: "SpotifySuccess", // MUST MATCH the URL path EXACTLY
      Profile: "profile",
    },
  },
};
 
export default function App() {
  return (
    <SafeAreaProvider>
      <NavigationContainer linking={linking}>
        <Stack.Navigator
          initialRouteName="Login"
          screenOptions={{ headerShown: false }}
        >
          <Stack.Screen name="Login" component={LoginScreen} />
          <Stack.Screen name="Signup" component={SignupScreen} />
          <Stack.Screen name="Onboarding" component={onboarding} />
          <Stack.Screen name="Quiz" component={QuizScreen} />
          <Stack.Screen name="Results" component={ResultsScreen} />
          <Stack.Screen
            name="SpotifySuccess"
            component={SpotifySuccessScreen}
          />
          <Stack.Screen name="Profile" component={ProfileScreen} />
        </Stack.Navigator>
        <StatusBar style="auto" />
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
 
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
});