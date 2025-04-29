//
//  LandmarksApp.swift
//  Landmarks
//
//  Created by Claire McManus  on 4/14/25.
//

import SwiftUI


@main
struct LandmarksApp: App {
    @State private var modelData = ModelData()


    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(modelData)
        }
    }
}
