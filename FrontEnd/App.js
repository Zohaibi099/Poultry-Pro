import React from 'react';
import 'react-native-gesture-handler';
import 'react-native-reanimated';
import { NavigationContainer } from "@react-navigation/native";
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { store, persistor } from './redux/store/store';
import RootNavigator from './navigation/RootNavigator';
import * as Linking from 'expo-linking';

const linking = {
  prefixes: [Linking.createURL('/')],
  config: {
    screens: {
      MainApp: {
        screens: {
          Profile: {
            screens: {
              ProfileMain: {
                path: 'profile/:userId',
              },
            },
          },
        },
      },
    },
  },
};

export default function App() {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <SafeAreaProvider>
          <NavigationContainer linking={linking}>
            <RootNavigator />
          </NavigationContainer>
        </SafeAreaProvider>
      </PersistGate>
    </Provider>
  );
}