/*
 * Simple WebRTC PeerConnection Demo
 * Demonstrates basic PeerConnection creation and configuration
 */

#include <iostream>
#include <memory>
#include <string>

#include "api/create_peerconnection_factory.h"
#include "api/peer_connection_interface.h"
#include "api/scoped_refptr.h"
#include "api/task_queue/default_task_queue_factory.h"
#include "rtc_base/thread.h"
#include "rtc_base/logging.h"

// Simple observer for PeerConnection events
class DummyPCO : public webrtc::PeerConnectionObserver {
 public:
  void OnSignalingChange(
      webrtc::PeerConnectionInterface::SignalingState new_state) override {
    std::cout << "Signaling state changed: " << new_state << std::endl;
  }

  void OnAddTrack(
      rtc::scoped_refptr<webrtc::RtpReceiverInterface> receiver,
      const std::vector<rtc::scoped_refptr<webrtc::MediaStreamInterface>>&
          streams) override {
    std::cout << "Track added: " << receiver->id() << std::endl;
  }

  void OnRemoveTrack(
      rtc::scoped_refptr<webrtc::RtpReceiverInterface> receiver) override {
    std::cout << "Track removed: " << receiver->id() << std::endl;
  }

  void OnDataChannel(
      rtc::scoped_refptr<webrtc::DataChannelInterface> channel) override {
    std::cout << "Data channel created: " << channel->label() << std::endl;
  }

  void OnRenegotiationNeeded() override {
    std::cout << "Renegotiation needed" << std::endl;
  }

  void OnIceConnectionChange(
      webrtc::PeerConnectionInterface::IceConnectionState new_state) override {
    std::cout << "ICE connection state: " << new_state << std::endl;
  }

  void OnIceGatheringChange(
      webrtc::PeerConnectionInterface::IceGatheringState new_state) override {
    std::cout << "ICE gathering state: " << new_state << std::endl;
  }

  void OnIceCandidate(const webrtc::IceCandidateInterface* candidate) override {
    std::cout << "ICE candidate: " << candidate->sdp_mline_index() << std::endl;
  }
};

// Simple session description observer
class DummySDO : public webrtc::SetSessionDescriptionObserver {
 public:
  void OnSuccess() override {
    std::cout << "Set session description success" << std::endl;
  }

  void OnFailure(webrtc::RTCError error) override {
    std::cout << "Set session description failed: " << error.message() << std::endl;
  }
};

// Simple create session description observer
class DummyCSDO : public webrtc::CreateSessionDescriptionObserver {
 public:
  void OnSuccess(webrtc::SessionDescriptionInterface* desc) override {
    std::cout << "Create session description success" << std::endl;
    std::string sdp;
    desc->ToString(&sdp);
    std::cout << "SDP: " << sdp.substr(0, 100) << "..." << std::endl;
  }

  void OnFailure(webrtc::RTCError error) override {
    std::cout << "Create session description failed: " << error.message()
              << std::endl;
  }
};

int main(int argc, char* argv[]) {
  std::cout << "WebRTC PeerConnection Demo" << std::endl;
  std::cout << "==========================" << std::endl;

  // Create signaling thread
  std::unique_ptr<webrtc::Thread> signaling_thread = webrtc::Thread::CreateWithSocketServer();
  signaling_thread->Start();

  // Create network thread
  std::unique_ptr<webrtc::Thread> network_thread = webrtc::Thread::CreateWithSocketServer();
  network_thread->Start();

  // Create worker thread
  std::unique_ptr<webrtc::Thread> worker_thread = webrtc::Thread::Create();
  worker_thread->Start();

  // Create task queue factory
  std::unique_ptr<webrtc::TaskQueueFactory> task_queue_factory =
      webrtc::CreateDefaultTaskQueueFactory();

  // Create peer connection factory dependencies
  webrtc::PeerConnectionFactoryDependencies deps;
  deps.signaling_thread = signaling_thread.get();
  deps.network_thread = network_thread.get();
  deps.worker_thread = worker_thread.get();
  deps.task_queue_factory = std::move(task_queue_factory);

  // Note: For a full implementation, you would set up audio/video codecs here
  // This is a minimal example

  std::cout << "Creating PeerConnectionFactory..." << std::endl;
  rtc::scoped_refptr<webrtc::PeerConnectionFactoryInterface> factory =
      webrtc::CreateModularPeerConnectionFactory(std::move(deps));

  if (!factory) {
    std::cerr << "Failed to create PeerConnectionFactory!" << std::endl;
    return 1;
  }

  std::cout << "PeerConnectionFactory created successfully!" << std::endl;

  // Create peer connection observer
  DummyPCO observer;

  // Create peer connection configuration
  webrtc::PeerConnectionInterface::RTCConfiguration config;
  config.sdp_semantics = webrtc::SdpSemantics::kUnifiedPlan;

  // Add STUN server (Google's public STUN server)
  webrtc::PeerConnectionInterface::IceServer stun_server;
  stun_server.uri = "stun:stun.l.google.com:19302";
  config.servers.push_back(stun_server);

  std::cout << "Creating PeerConnection..." << std::endl;

  // Create peer connection dependencies
  webrtc::PeerConnectionDependencies pc_deps(&observer);

  // Create peer connection
  auto result_or_error = factory->CreatePeerConnectionOrError(
      config, std::move(pc_deps));

  if (!result_or_error.ok()) {
    std::cerr << "Failed to create PeerConnection: "
              << result_or_error.error().message() << std::endl;
    return 1;
  }

  rtc::scoped_refptr<webrtc::PeerConnectionInterface> pc =
      result_or_error.MoveValue();

  std::cout << "PeerConnection created successfully!" << std::endl;

  // Print peer connection statistics
  std::cout << std::endl << "PeerConnection Statistics:" << std::endl;
  std::cout << "  Signaling State: " << pc->signaling_state() << std::endl;
  std::cout << "  ICE Connection State: " << pc->ice_connection_state()
            << std::endl;
  std::cout << "  ICE Gathering State: " << pc->ice_gathering_state()
            << std::endl;

  std::cout << std::endl << "Demo completed successfully!" << std::endl;
  std::cout << "PeerConnection was created and is ready to use." << std::endl;

  return 0;
}
