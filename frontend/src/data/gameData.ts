import { RoleData, Role } from "../types/gameTypes";

export const gameData: Record<Role, RoleData> = {
  SDE: {
    id: "SDE",
    name: "Software Development Engineer",
    description:
      "Master coding interviews, system design, and algorithmic thinking",
    icon: "💻",
    levels: [
      {
        id: "sde-beginner",
        name: "Algorithm Apprentice",
        level: "beginner",
        unlocked: true,
        completed: false,
        stars: 0,
        boss: {
          id: "algo-junior",
          name: "Junior Algorithm Bot",
          avatar: "🤖",
          hp: 80,
          questions: [
            "What is the time complexity of binary search?",
            "Explain the difference between array and linked list.",
            "How do you reverse a string in place?",
            "What is the purpose of the 'this' keyword in JavaScript?",
            "Describe how bubble sort works.",
          ],
          responses: {
            excellent: [
              "Outstanding! Your logic is flawless!",
              "Perfect explanation! You've mastered this concept!",
              "Excellent work! That's exactly right!",
            ],
            good: [
              "Good answer, but could be more precise.",
              "Not bad, but there's room for improvement.",
              "Decent response, keep going!",
            ],
            poor: [
              "Weak attempt! Think harder!",
              "That's not quite right. Try again!",
              "Your understanding needs work!",
            ],
            victory:
              "Impossible! A mere beginner has defeated me! Well done, future engineer!",
          },
        },
      },
      {
        id: "sde-intermediate",
        name: "System Architect",
        level: "intermediate",
        unlocked: false,
        completed: false,
        stars: 0,
        boss: {
          id: "system-senior",
          name: "Senior System Architect",
          avatar: "⚙️",
          hp: 120,
          questions: [
            "Design a URL shortener like bit.ly. What are the key components?",
            "How would you handle race conditions in a multi-threaded environment?",
            "Explain the CAP theorem and its implications.",
            "Design a rate limiter for an API. What algorithms would you use?",
            "How would you implement a distributed cache?",
          ],
          responses: {
            excellent: [
              "Brilliant system design! You think like a senior engineer!",
              "Exceptional architecture! Your scalability considerations are spot-on!",
              "Outstanding! That's exactly how I'd approach it!",
            ],
            good: [
              "Solid approach, but consider edge cases.",
              "Good foundation, but what about scalability?",
              "Decent design, but think about trade-offs.",
            ],
            poor: [
              "Amateur thinking! Real systems need more consideration!",
              "That won't scale! Think bigger!",
              "Your design has critical flaws!",
            ],
            victory:
              "Remarkable! You've outdesigned a senior architect! You're ready for the next level!",
          },
        },
      },
      {
        id: "sde-expert",
        name: "Tech Lead Master",
        level: "expert",
        unlocked: false,
        completed: false,
        stars: 0,
        boss: {
          id: "tech-lead",
          name: "Elite Tech Lead",
          avatar: "👑",
          hp: 150,
          questions: [
            "You're tasked with migrating a monolithic application to microservices. Outline your strategy.",
            "How would you design a real-time collaborative editing system like Google Docs?",
            "Explain how you'd architect a system to handle 1 billion daily active users.",
            "Design a global content delivery network with automatic failover.",
            "How would you optimize database performance for a system with 100TB of data?",
          ],
          responses: {
            excellent: [
              "Masterful! You understand enterprise-scale architecture!",
              "Genius-level thinking! That's exactly how tech leads solve problems!",
              "Perfect! You've demonstrated true technical leadership!",
            ],
            good: [
              "Good technical depth, but consider business impact.",
              "Technically sound, but what about team coordination?",
              "Solid engineering, but think about long-term maintenance.",
            ],
            poor: [
              "A tech lead would never propose such a naive solution!",
              "Your approach lacks the sophistication needed at this level!",
              "That's not enterprise-grade thinking!",
            ],
            victory:
              "Inconceivable! You've surpassed even my expertise! You are a true technical leader!",
          },
        },
      },
    ],
  },
};