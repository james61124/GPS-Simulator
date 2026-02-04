import SwiftUI

struct ContentView: View {
    var body: some View {
        Text("Writing 20 steps every 10 seconds")
            .onAppear {
                HealthManager.shared.requestHealthAuth()
                HealthManager.shared.startWritingFixedSteps()
            }
    }
}

#Preview {
    ContentView()
}
