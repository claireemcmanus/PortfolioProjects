//
//  ContentView.swift
//  States2
//
//  Created by Claire McManus  on 4/7/25.
//

import SwiftUI

struct ContentView: View {
    let states  = [ "(AK) Alaska", "(AL) Alabama", "(AR) Arkansas", "(AS) American Samoa", "(AZ) Arizona", "(CA) California", "(CO) Colorado", "(CT) Connecticut", "(DC) District of Columbia", "(DE) Delaware", "(FL) Florida", "(GA) Georgia", "(GU) Guam", "(HI) Hawaii", "(IA) Iowa", "(ID) Idaho", "(IL) Illinois", "(IN) Indiana", "(KS) Kansas", "(KY) Kentucky", "(LA) Louisiana", "(MA) Massachusetts", "(MD) Maryland", "(ME) Maine", "(MI) Michigan", "(MN) Minnesota", "(MO) Missouri", "(MS) Mississippi", "(MT) Montana", "(NC) North Carolina", "(ND) North Dakota", "(NE) Nebraska", "(NH) New Hampshire", "(NJ) New Jersey", "(NM) New Mexico", "(NV) Nevada", "(NY) New York", "(OH) Ohio", "(OK) Oklahoma", "(OR) Oregon", "(PA) Pennsylvania", "(PR) Puerto Rico", "(RI) Rhode Island", "(SC) South Carolina", "(SD) South Dakota", "(TN) Tennessee", "(TX) Texas", "(UT) Utah", "(VA) Virginia", "(VI) Virgin Islands", "(VT) Vermont", "(WA) Washington", "(WI) Wisconsin", "(WV) West Virginia", "(WY) Wyoming" ]
    
    @State private var selectedState = "(AK) Alaska"
        @State private var showPicker = false
        
        var body: some View {
            VStack(spacing: 20) {
                Spacer()
                Text(selectedState)
                    .font(.title3)
                    .foregroundColor(.blue)
                    .onTapGesture {
                        showPicker = true
                    }
                
                if showPicker {
                    Picker("State", selection: $selectedState) {
                        ForEach(states, id: \.self) { state in
                            Text(state)
                        }
                    }
                    .pickerStyle(.wheel)
                }
                
                Text("Selected state: \(selectedState)")
                    .font(.title2)
                
                Spacer()
            }
            .padding()
        }
}

#Preview {
    ContentView()
}
