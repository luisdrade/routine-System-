import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, StatusBar } from 'react-native';
import { useFonts, BebasNeue_400Regular } from '@expo-google-fonts/bebas-neue';
import { Inter_400Regular, Inter_700Bold } from '@expo-google-fonts/inter';
import * as SplashScreen from 'expo-splash-screen';

// Segura a tela de splash até as fontes carregarem
SplashScreen.preventAutoHideAsync();

export default function App() {
  const [setsCompleted, setSetsCompleted] = useState(0);
  
  const [fontsLoaded] = useFonts({
    BebasNeue: BebasNeue_400Regular,
    Inter: Inter_400Regular,
    InterBold: Inter_700Bold,
  });

  useEffect(() => {
    if (fontsLoaded) {
      SplashScreen.hideAsync();
    }
  }, [fontsLoaded]);

  if (!fontsLoaded) {
    return null;
  }

  const handleCompleteSet = () => {
    setSetsCompleted(prev => prev + 1);
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#121212" />
      
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>SUPINO RETO</Text>
        <Text style={styles.subtitle}>Série {setsCompleted + 1} de 4</Text>
      </View>

      {/* Info Rápida */}
      <View style={styles.infoRow}>
        <View style={styles.infoBox}>
          <Text style={styles.infoLabel}>CARGA</Text>
          <Text style={styles.infoValue}>80 KG</Text>
        </View>
        <View style={styles.infoBox}>
          <Text style={styles.infoLabel}>ALVO RPE</Text>
          <Text style={styles.infoValue}>8.0</Text>
        </View>
      </View>

      {/* Botão Gigante de Ação */}
      <View style={styles.actionContainer}>
        <TouchableOpacity 
          style={styles.mainButton}
          activeOpacity={0.8}
          onPress={handleCompleteSet}
        >
          <Text style={styles.mainButtonText}>COMPLETAR SÉRIE</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212', // Fundo bem escuro
    paddingHorizontal: 24,
    paddingTop: 80,
  },
  header: {
    marginBottom: 40,
  },
  title: {
    fontFamily: 'BebasNeue',
    fontSize: 56,
    color: '#FFFFFF',
    textTransform: 'uppercase',
  },
  subtitle: {
    fontFamily: 'Inter',
    fontSize: 18,
    color: '#A0A0A0', // Cinza claro
    marginTop: 4,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 60,
  },
  infoBox: {
    backgroundColor: '#1E1E1E',
    padding: 20,
    borderRadius: 12,
    flex: 0.48,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#333333',
  },
  infoLabel: {
    fontFamily: 'InterBold',
    fontSize: 12,
    color: '#A0A0A0',
    marginBottom: 8,
  },
  infoValue: {
    fontFamily: 'BebasNeue',
    fontSize: 40,
    color: '#FF5722', // Laranja vibrante
  },
  actionContainer: {
    flex: 1,
    justifyContent: 'flex-end',
    paddingBottom: 40,
  },
  mainButton: {
    backgroundColor: '#FF5722', // Laranja vibrante
    height: 120, // Botão gigante para área de clique
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#FF5722',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 10,
  },
  mainButtonText: {
    fontFamily: 'BebasNeue',
    fontSize: 48,
    color: '#FFFFFF',
  }
});
