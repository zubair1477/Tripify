// screens/OnboardingScreen.tsx
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';

export default function OnboardingScreen({ navigation }: any) {
  const handleNext = () => {
   
    console.log('Next button pressed');
    navigation.navigate('Quiz'); 
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        {/* Icon Circle */}
        <View style={styles.iconContainer}>
          <Text style={styles.iconText}>🎵</Text>
        </View>

        <Text style={styles.title}>Let's find your vibe</Text>

        <Text style={styles.description}>
          Answer a few questions to discover music that matches your personality and mood
        </Text>

        {/* What to Expect Box */}
        <View style={styles.expectBox}>
          <Text style={styles.expectTitle}>What to Expect</Text>

          <View style={styles.stepContainer}>
            <View style={styles.stepCircle}>
              <Text style={styles.stepNumber}>1</Text>
            </View>
            <Text style={styles.stepText}>Tell us how you're feeling</Text>
          </View>

          <View style={styles.stepContainer}>
            <View style={styles.stepCircle}>
              <Text style={styles.stepNumber}>2</Text>
            </View>
            <Text style={styles.stepText}>Share where you're going</Text>
          </View>

          <View style={styles.stepContainer}>
            <View style={styles.stepCircle}>
              <Text style={styles.stepNumber}>3</Text>
            </View>
            <Text style={styles.stepText}>Get your custom playlist</Text>
          </View>
        </View>
      </View>

      {/* Next Button */}
      <TouchableOpacity style={styles.nextButton} onPress={handleNext}>
        <Text style={styles.nextButtonText}>Next</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    padding: 24,
    justifyContent: 'space-between',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  iconContainer: {
    width: 140,
    height: 140,
    borderRadius: 70,
    backgroundColor: '#3BF664',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 32,
  },
  iconText: {
    fontSize: 60,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#1F2937',
    marginBottom: 16,
  },
  description: {
    fontSize: 16,
    textAlign: 'center',
    color: '#6B7280',
    lineHeight: 24,
    paddingHorizontal: 32,
    marginBottom: 32,
  },
  expectBox: {
    width: '100%',
    maxWidth: 400,
    padding: 24,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#E5E7EB',
    backgroundColor: '#F9FAFB',
    gap: 16,
  },
  expectTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1F2937',
    marginBottom: 8,
  },
  stepContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  stepCircle: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#3BF664',
    alignItems: 'center',
    justifyContent: 'center',
  },
  stepNumber: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  stepText: {
    flex: 1,
    fontSize: 15,
    color: '#374151',
  },
  nextButton: {
    backgroundColor: '#3BF664',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 32,
  },
  nextButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});