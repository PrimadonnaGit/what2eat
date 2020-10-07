import React, { Component } from 'react';
import { StyleSheet, Text, View, ScrollView, TextInput, SafeAreaView, Button, Alert } from 'react-native';

class APP extends Component {
  constructor(props) {
    super(props);
    this.state = {
      titleText: "Smart Shopping Basket",
      bodyText: "스마트 장바구니",
      inputText: "레시피를 입력하세요."
    };
  }

  render() {
    return (
      <View style={styles.container}>
        <View style={styles.header}><Text>header</Text></View>
        <View style={styles.title}><Text>title</Text></View>
        <View style={styles.content}><Text>content</Text></View>
        <View style={styles.footer}></View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,

  },
  header: {
    flex: 0.45, // 0.75 - 0.45
    backgroundColor: 'red',
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    flex: 1,
    backgroundColor: 'yellow',
    justifyContent: 'center',
    alignItems: 'center',

  },
  content: {
    flex: 1,
    backgroundColor: 'green',
    justifyContent: 'center',
    alignItems: 'center',
  },
  footer: {
    flex: 0.25,
    backgroundColor: 'blue',
    justifyContent: 'center',
    alignItems: 'center',

  },

});

export default APP;

