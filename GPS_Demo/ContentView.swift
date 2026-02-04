import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Hello, world!")
        }
        .padding()
    }
    // var body: some View {
    //     Text("Writing 20 steps every 10 seconds")
    //         .onAppear {
    //             HealthManager.shared.requestHealthAuth()
    //             HealthManager.shared.startWritingFixedSteps()
    //         }
    // }
}

#Preview {
    ContentView()
}
