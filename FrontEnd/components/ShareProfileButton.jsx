import React from 'react';
import { TouchableOpacity, Text, Share, StyleSheet, View, Platform } from 'react-native';
import { Feather } from '@expo/vector-icons';
import * as Linking from 'expo-linking';
import Constants from 'expo-constants';

const ShareProfileButton = ({ seller }) => {
  const handleShareProfile = async () => {
    try {
      if (!seller) return;

      let profileUrl;
      
      // Use custom scheme for dev client and production, expo link for Expo Go
      if (Constants.appOwnership === 'expo') {
        // We are in the Expo Go app, use the expo deep link
        profileUrl = Linking.createURL(`profile/${seller.id}`);
      } else {
        // We are in a standalone app (dev client or production build)
        profileUrl = `poultrypro://profile/${seller.id}`;
      }

      await Share.share({
        message: `Check out ${seller.business_name || seller.full_name}'s poultry profile on PoultryPro: ${profileUrl}`,
        url: profileUrl, // for iOS
        title: `Share ${seller.business_name || seller.full_name}'s Profile`
      });
    } catch (error) {
      console.log('Error sharing profile:', error.message);
    }
  };

  return (
    <TouchableOpacity
      style={styles.quickAction}
      onPress={handleShareProfile}
    >
      <View style={[styles.quickActionIcon, { backgroundColor: '#3498DB' }]}>
        <Feather name="share-2" size={24} color="white" />
      </View>
      <Text style={styles.quickActionText}>Share Profile</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  quickAction: {
    alignItems: 'center',
    flex: 1,
  },
  quickActionIcon: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
  },
  quickActionText: {
    fontSize: 13,
    color: '#2C3E50',
    fontWeight: '600',
    textAlign: 'center',
  },
});

export default ShareProfileButton;