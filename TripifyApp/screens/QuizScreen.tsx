// screens/QuizScreen.tsx
import { useState } from "react";
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Alert,
  ActivityIndicator,
} from "react-native";
import { quizQuestions } from "../Quiz/quiz-data";
import { calculateMood } from "../services/quizService";

export default function QuizScreen({ navigation, route }: any) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<{ [key: number]: number }>({});
  const [loading, setLoading] = useState(false);

  // Get userId from route params (passed from login/signup)
  const userId = route?.params?.userId;

  const question = quizQuestions[currentQuestion];
  const isLastQuestion = currentQuestion === quizQuestions.length - 1;
  const isFirstQuestion = currentQuestion === 0;

  const handleSelectOption = (optionIndex: number) => {
    setAnswers({ ...answers, [currentQuestion]: optionIndex });
  };

  const handleNext = async () => {
    if (isLastQuestion) {
      // Submit quiz to backend and calculate mood
      setLoading(true);
      try {
        console.log("Submitting quiz answers:", answers);

        const moodResult = await calculateMood({
          userId: userId || "guest",
          answers: answers,
        });

        console.log("Mood calculation result:", moodResult);

        // Navigate to results screen with mood data
        navigation.navigate("Results", {
          answers,
          moodResult,
          userId: userId || "guest",
        });
      } catch (error) {
        console.error("Error submitting quiz:", error);
        Alert.alert(
          "Error",
          "Failed to calculate your mood. Please try again.",
          [{ text: "OK" }]
        );
      } finally {
        setLoading(false);
      }
    } else {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handleBack = () => {
    if (!isFirstQuestion) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const selectedOption = answers[currentQuestion];

  return (
    <View style={styles.container}>
      {/* Header with Progress */}
      <View style={styles.header}>
        <Text style={styles.questionNumber}>
          Question {currentQuestion + 1} of {quizQuestions.length}
        </Text>
        <View style={styles.progressBar}>
          <View
            style={[
              styles.progressFill,
              {
                width: `${
                  ((currentQuestion + 1) / quizQuestions.length) * 100
                }%`,
              },
            ]}
          />
        </View>
      </View>

      {/* Question and Options */}
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <Text style={styles.question}>{question.question}</Text>

        <View style={styles.optionsContainer}>
          {question.options.map((option, index) => (
            <TouchableOpacity
              key={index}
              style={[
                styles.optionButton,
                selectedOption === index && styles.optionButtonSelected,
              ]}
              onPress={() => handleSelectOption(index)}
            >
              <View
                style={[
                  styles.radioCircle,
                  selectedOption === index && styles.radioCircleSelected,
                ]}
              >
                {selectedOption === index && <View style={styles.radioInner} />}
              </View>
              <Text style={styles.optionText}>{option}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>

      {/* Navigation Buttons */}
      <View style={styles.navigationButtons}>
        <TouchableOpacity
          style={[
            styles.navButton,
            styles.backButton,
            (isFirstQuestion || loading) && styles.disabledButton,
          ]}
          onPress={handleBack}
          disabled={isFirstQuestion || loading}
        >
          <Text
            style={[
              styles.backButtonText,
              (isFirstQuestion || loading) && styles.disabledText,
            ]}
          >
            ← Back
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[
            styles.navButton,
            styles.nextButton,
            (selectedOption === undefined || loading) && styles.disabledButton,
          ]}
          onPress={handleNext}
          disabled={selectedOption === undefined || loading}
        >
          {loading ? (
            <ActivityIndicator color="#FFFFFF" />
          ) : (
            <Text style={styles.nextButtonText}>
              {isLastQuestion ? "Finish" : "Next →"}
            </Text>
          )}
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFFFFF",
  },
  header: {
    padding: 24,
    paddingTop: 60,
  },
  questionNumber: {
    fontSize: 14,
    color: "#6B7280",
    marginBottom: 12,
  },
  progressBar: {
    height: 4,
    backgroundColor: "#E5E7EB",
    borderRadius: 2,
    overflow: "hidden",
  },
  progressFill: {
    height: "100%",
    backgroundColor: "#3BF664",
    borderRadius: 2,
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
  },
  question: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#1F2937",
    marginBottom: 32,
    lineHeight: 36,
  },
  optionsContainer: {
    gap: 12,
    paddingBottom: 24,
  },
  optionButton: {
    flexDirection: "row",
    alignItems: "center",
    padding: 16,
    borderRadius: 12,
    gap: 12,
    backgroundColor: "#F9FAFB",
    borderWidth: 1,
    borderColor: "#E5E7EB",
  },
  optionButtonSelected: {
    borderColor: "#3BF664",
    borderWidth: 2,
    backgroundColor: "#F0FDF4",
  },
  radioCircle: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: "#E5E7EB",
    alignItems: "center",
    justifyContent: "center",
  },
  radioCircleSelected: {
    borderColor: "#3BF664",
  },
  radioInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: "#3BF664",
  },
  optionText: {
    flex: 1,
    fontSize: 16,
    color: "#1F2937",
  },
  navigationButtons: {
    flexDirection: "row",
    padding: 24,
    gap: 12,
  },
  navButton: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 16,
    borderRadius: 12,
  },
  backButton: {
    backgroundColor: "#F9FAFB",
    borderWidth: 1,
    borderColor: "#E5E7EB",
  },
  backButtonText: {
    fontSize: 16,
    fontWeight: "600",
    color: "#374151",
  },
  nextButton: {
    backgroundColor: "#3BF664",
  },
  nextButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
  disabledButton: {
    opacity: 0.5,
  },
  disabledText: {
    color: "#9CA3AF",
  },
});
