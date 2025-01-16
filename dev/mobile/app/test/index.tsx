import {Platform} from 'react-native';

import {HelloWave} from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import {ThemedText} from '@/components/ThemedText';

import { useSelector } from "react-redux";
import { selectUserId } from '@/redux/features/users/usersSelectors';

export default function HomeScreen(){
    // 状態変数の取得
    const userId = useSelector(selectUserId);
    console.log("userId:", userId);

    return (
        <ParallaxScrollView
            headerBackgroundColor={{light:'#A1CEDC',dark:'#1D3D47'}}>
            <ThemedText>
                Kodomori!
            </ThemedText>
            <HelloWave/>
            <ThemedText>
                Step 1: Make home page
            </ThemedText>
            <ThemedText>
                Step 2: Make vision larning
            </ThemedText>
            <ThemedText>
                Step 3: Make sound learning
            </ThemedText>

        </ParallaxScrollView>

    )
}