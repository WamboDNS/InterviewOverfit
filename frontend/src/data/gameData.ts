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

  DS: {
    id: "DS",
    name: "Data Scientist",
    description:
      "Conquer machine learning, statistics, and data analysis challenges",
    icon: "📊",
    levels: [
      {
        id: "ds-beginner",
        name: "Data Explorer",
        level: "beginner",
        unlocked: true,
        completed: false,
        stars: 0,
        boss: {
          id: "stats-junior",
          name: "Statistics Novice",
          avatar: "📈",
          hp: 80,
          questions: [
            "What's the difference between mean, median, and mode?",
            "Explain what a p-value represents in hypothesis testing.",
            "How do you handle missing data in a dataset?",
            "What is the difference between correlation and causation?",
            "Explain the concept of overfitting in machine learning.",
          ],
          responses: {
            excellent: [
              "Excellent statistical understanding!",
              "Perfect! Your data intuition is strong!",
              "Outstanding analysis! You think like a true data scientist!",
            ],
            good: [
              "Good foundation, but dig deeper into the theory.",
              "Solid understanding, but consider practical implications.",
              "Decent grasp, but explore edge cases.",
            ],
            poor: [
              "Your statistical knowledge needs serious work!",
              "That's not how data science works!",
              "Basic concepts are clearly not understood!",
            ],
            victory:
              "Amazing! You've mastered the fundamentals! Ready for more complex challenges!",
          },
        },
      },
      {
        id: "ds-intermediate",
        name: "ML Engineer",
        level: "intermediate",
        unlocked: false,
        completed: false,
        stars: 0,
        boss: {
          id: "ml-senior",
          name: "Senior ML Engineer",
          avatar: "🧠",
          hp: 120,
          questions: [
            "Explain the bias-variance tradeoff and how to balance it.",
            "How would you design an A/B testing framework for a recommendation system?",
            "Compare gradient boosting and random forests. When would you use each?",
            "How do you evaluate the performance of an unsupervised learning model?",
            "Explain how backpropagation works in neural networks.",
          ],
          responses: {
            excellent: [
              "Brilliant ML understanding! You grasp the nuances!",
              "Exceptional! Your model thinking is advanced!",
              "Perfect explanation! You understand both theory and practice!",
            ],
            good: [
              "Good ML knowledge, but consider production constraints.",
              "Solid approach, but think about model interpretability.",
              "Decent understanding, but what about scalability?",
            ],
            poor: [
              "Your ML knowledge is superficial at best!",
              "That approach would fail in production!",
              "You're missing fundamental ML principles!",
            ],
            victory:
              "Incredible! You've outperformed a senior ML engineer! Your expertise is undeniable!",
          },
        },
      },
      {
        id: "ds-expert",
        name: "AI Research Lead",
        level: "expert",
        unlocked: false,
        completed: false,
        stars: 0,
        boss: {
          id: "ai-researcher",
          name: "AI Research Director",
          avatar: "🔬",
          hp: 150,
          questions: [
            "Design a novel architecture for few-shot learning in computer vision.",
            "How would you approach building a multimodal AI system that understands text, images, and audio?",
            "Explain your strategy for detecting and mitigating bias in large language models.",
            "Design an experiment to evaluate the causal impact of a recommendation algorithm.",
            "How would you architect a real-time ML system that serves 100M predictions per second?",
          ],
          responses: {
            excellent: [
              "Revolutionary thinking! You're pushing the boundaries of AI!",
              "Genius-level research approach! That's publication-worthy!",
              "Extraordinary! You understand cutting-edge AI at the deepest level!",
            ],
            good: [
              "Strong research direction, but consider ethical implications.",
              "Good theoretical foundation, but think about reproducibility.",
              "Solid approach, but explore computational efficiency.",
            ],
            poor: [
              "That's not research-grade thinking!",
              "Your approach lacks the rigor expected at this level!",
              "Amateur hour! Real AI research requires deeper understanding!",
            ],
            victory:
              "Unbelievable! You've surpassed even my research capabilities! You are a true AI visionary!",
          },
        },
      },
    ],
  },

  MLE: {
    id: "MLE",
    name: "Machine Learning Engineer",
    description:
      "Deploy, scale, and optimize ML systems in production environments",
    icon: "⚡",
    levels: [
      {
        id: "mle-beginner",
        name: "Model Deployer",
        level: "beginner",
        unlocked: true,
        completed: false,
        stars: 0,
        boss: {
          id: "deploy-junior",
          name: "Junior MLOps Engineer",
          avatar: "🚀",
          hp: 80,
          questions: [
            "How do you deploy a machine learning model to production?",
            "What's the difference between batch and real-time inference?",
            "Explain model versioning and why it's important.",
            "How do you monitor model performance in production?",
            "What are the key considerations for ML model security?",
          ],
          responses: {
            excellent: [
              "Perfect deployment strategy! You understand production ML!",
              "Excellent! Your MLOps knowledge is solid!",
              "Outstanding! That's exactly how you productionize models!",
            ],
            good: [
              "Good approach, but consider monitoring edge cases.",
              "Solid foundation, but think about model drift.",
              "Decent strategy, but what about rollback procedures?",
            ],
            poor: [
              "That deployment would fail immediately!",
              "You don't understand production constraints!",
              "Basic MLOps concepts are clearly missing!",
            ],
            victory:
              "Impressive! You've mastered ML deployment fundamentals! Ready for scaling challenges!",
          },
        },
      },
      {
        id: "mle-intermediate",
        name: "Infrastructure Optimizer",
        level: "intermediate",
        unlocked: false,
        completed: false,
        stars: 0,
        boss: {
          id: "infra-senior",
          name: "Senior Infrastructure Engineer",
          avatar: "⚙️",
          hp: 120,
          questions: [
            "Design a feature store for a large-scale ML platform.",
            "How would you optimize inference latency for a deep learning model?",
            "Explain your approach to ML model A/B testing in production.",
            "How do you handle data pipeline failures in a real-time ML system?",
            "Design an auto-scaling solution for ML workloads.",
          ],
          responses: {
            excellent: [
              "Brilliant infrastructure design! You think at scale!",
              "Exceptional optimization! Your performance tuning is expert-level!",
              "Perfect! You understand enterprise ML infrastructure!",
            ],
            good: [
              "Good scalability thinking, but consider cost optimization.",
              "Solid approach, but what about fault tolerance?",
              "Decent design, but think about multi-region deployment.",
            ],
            poor: [
              "That infrastructure won't handle production load!",
              "Your optimization approach is naive!",
              "You're missing critical scaling considerations!",
            ],
            victory:
              "Remarkable! You've optimized beyond my capabilities! Your infrastructure expertise is exceptional!",
          },
        },
      },
      {
        id: "mle-expert",
        name: "ML Platform Architect",
        level: "expert",
        unlocked: false,
        completed: false,
        stars: 0,
        boss: {
          id: "platform-architect",
          name: "ML Platform Architect",
          avatar: "🏗️",
          hp: 150,
          questions: [
            "Design a complete MLOps platform supporting the entire ML lifecycle for 1000+ data scientists.",
            "How would you architect a multi-cloud ML platform with automatic model optimization?",
            "Design a system for federated learning across geographically distributed data centers.",
            "Create a strategy for managing ML model governance and compliance at enterprise scale.",
            "How would you build a platform that automatically detects and mitigates model bias in production?",
          ],
          responses: {
            excellent: [
              "Masterful platform architecture! You're a true ML infrastructure visionary!",
              "Genius-level systems thinking! That's how you build the future of ML!",
              "Extraordinary! You understand ML platforms at the deepest architectural level!",
            ],
            good: [
              "Strong platform thinking, but consider developer experience.",
              "Good architecture, but think about operational complexity.",
              "Solid design, but explore vendor lock-in mitigation.",
            ],
            poor: [
              "That platform architecture is fundamentally flawed!",
              "You don't understand enterprise ML platform requirements!",
              "That's not platform-grade thinking!",
            ],
            victory:
              "Inconceivable! You've out-architected the master! You are the ultimate ML platform visionary!",
          },
        },
      },
    ],
  },
};