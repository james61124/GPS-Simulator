import SwiftUI

struct ContentView: View {
    // State to store the number of steps entered by the user
    @State private var stepsInput: String = ""
    
    // State to control the visibility of the success feedback message
    @State private var showSuccessMessage: Bool = false
    
    // State to store the amount that was successfully added for display
    @State private var successAmount: String = ""

    var body: some View {
        VStack(spacing: 30) {
            // Header Section: Visual identity of the app
            VStack(spacing: 12) {
                Image(systemName: "figure.walk.circle.fill")
                    .font(.system(size: 70))
                    .foregroundColor(.blue)
                
                Text("Health Simulator")
                    .font(.largeTitle)
                    .fontWeight(.bold)
            }
            .padding(.top, 50)
            
            // Feedback UI: Show a success message when steps are written to HealthKit
            if showSuccessMessage {
                HStack {
                    Image(systemName: "checkmark.circle.fill")
                    Text("Successfully added \(successAmount) steps!")
                }
                .font(.headline)
                .foregroundColor(.green)
                .padding()
                .background(Color.green.opacity(0.1))
                .cornerRadius(12)
                // Transition effect for smooth appearance/disappearance
                .transition(.asymmetric(insertion: .scale.combined(with: .opacity), removal: .opacity))
            }

            // Input Section: Where user defines the amount of steps
            VStack(alignment: .leading, spacing: 10) {
                Text("Steps to add:")
                    .font(.headline)
                    .foregroundColor(.secondary)
                
                TextField("Enter amount", text: $stepsInput)
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(10)
                    // Ensure the numeric keypad is shown for convenience
                    .keyboardType(.numberPad)
            }
            .padding(.horizontal)
            
            // Action Button: Triggers the HealthKit write operation
            Button(action: {
                // Convert string input to Double before calling the manager
                if let count = Double(stepsInput) {
                    // Call the shared HealthManager instance to save data
                    HealthManager.shared.addBulkSteps(count: count) { success in
                        if success {
                            // Update UI state on successful write
                            self.successAmount = stepsInput
                            withAnimation(.spring()) {
                                showSuccessMessage = true
                            }
                            
                            // Automatically hide the success message after 3 seconds
                            DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                                withAnimation {
                                    showSuccessMessage = false
                                }
                            }
                        }
                    }
                }
            }) {
                HStack {
                    Image(systemName: "plus.circle.fill")
                    Text("Add Steps Now")
                }
                .font(.headline)
                .foregroundColor(.white)
                .padding()
                .frame(maxWidth: .infinity)
                .background(Color.blue)
                .cornerRadius(15)
                .shadow(color: .blue.opacity(0.3), radius: 5, x: 0, y: 5)
            }
            .padding(.horizontal)
            
            Spacer()
            
            // Footer Section: Important instructions for the user
            VStack(spacing: 4) {
                Text("Note: Please make sure 'Steps' permission is")
                Text("granted in Settings > Health > Data Access.")
            }
            .font(.caption)
            .foregroundColor(.gray)
            .multilineTextAlignment(.center)
            .padding(.bottom, 20)
        }
        .padding()
        .onAppear {
            // Prompt for HealthKit permissions as soon as the view appears
            HealthManager.shared.requestHealthAuthorization()
        }
        // Dismiss the keyboard when the user taps on the background
        .onTapGesture {
            UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
        }
    }
}

// Preview provider for Xcode design canvas
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}