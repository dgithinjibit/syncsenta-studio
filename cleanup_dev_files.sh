#!/bin/bash

# Cleanup Development Files Script
# Removes temporary completion, summary, and progress files before GitHub push

echo "🧹 Cleaning up development files..."
echo ""

# Root directory temporary files
echo "Removing root temporary files..."
rm -f ALL_FIXES_COMPLETE.md
rm -f CBC_AGENT_COMPLETION_SUMMARY.md
rm -f CBC_AGENT_IMPLEMENTATION_SUMMARY.md
rm -f CURRICULUM_AWARE_FIX.md
rm -f CURRICULUM_INTEGRATION_COMPLETE.md
rm -f DOCX_PDF_EXPORT_COMPLETE.md
rm -f EXAM_BACKEND_IMPLEMENTATION_COMPLETE.md
rm -f EXAM_RUNNER_IMPLEMENTATION_COMPLETE.md
rm -f GIKUYU_AGENT_IMPROVEMENTS.md
rm -f GIKUYU_AGENT_TESTING_GUIDE.md
rm -f GIKUYU_DATA_GENERATION_COMPLETE.md
rm -f GIKUYU_INTEGRATION_SUMMARY.md
rm -f GIKUYU_MODEL_TRAINING_STRATEGY.md
rm -f KENYA_LLM_INTEGRATION_SUMMARY.md
rm -f KIKUYU_GENERATOR_FINAL.md
rm -f KISWAHILI_METTA_FIX.md
rm -f MVP_PIVOT_SUMMARY.md
rm -f MWALIMU_AI_LANGUAGE_FIX.md
rm -f PERSONALIZED_LEARNING_SUMMARY.md
rm -f QUICK_FIX_SUMMARY.md
rm -f RUST_BACKEND_FIXES_COMPLETE.md
rm -f SCHEMER_BACKEND_IMPLEMENTATION_COMPLETE.md
rm -f SCHEMER_DATABASE_SCHEMA_COMPLETE.md
rm -f SCHEMER_INTEGRATION_PROGRESS.md
rm -f SCHEMER_WIZARD_IMPLEMENTATION_COMPLETE.md
rm -f SCHEME_CONTEXT_INTEGRATION_COMPLETE.md
rm -f SCHEME_LIBRARY_COMPLETE.md
rm -f SCHEME_SAVING_IMPLEMENTATION_COMPLETE.md
rm -f SECTION_11_COMPLETE.md
rm -f SECTION_13_COMPLETE.md
rm -f SECTION_4_5_COMPLETE.md
rm -f SECTION_7_COMPLETE.md
rm -f SYNTHESIS_TUTOR_IMPLEMENTATION_COMPLETE.md
rm -f SYNTHESIS_TUTOR_PHASE1_COMPLETE.md
rm -f TEACHER_EXAM_GENERATOR_COMPLETE.md
rm -f TEACHER_SIDE_IMPLEMENTATION_ANALYSIS.md

echo "✅ Root temporary files removed"
echo ""

# Backend temporary files
echo "Removing backend temporary files..."
rm -f backend/syncsenta-backend/TASK_*.md
rm -f backend/syncsenta-backend/QUICKSTART.md

echo "✅ Backend temporary files removed"
echo ""

# Studio temporary files
echo "Removing studio temporary files..."
rm -f studio/SYNTHESIS_TUTOR_DASHBOARD_PROGRESS.md

echo "✅ Studio temporary files removed"
echo ""

# Dataset generation temporary files
echo "Removing dataset generation temporary files..."
rm -f dataset-generation/kenya-llm-bench-v1/IMPLEMENTATION_SUMMARY.md
rm -f dataset-generation/kenya-llm-bench-v1/DATASET_COMPLETION_SUMMARY.md
rm -f dataset-generation/kenya-llm-bench-v1/ENHANCED_CURRICULUM_SUMMARY.md

echo "✅ Dataset generation temporary files removed"
echo ""

# AI training temporary files (keep the important ones)
echo "Checking ai-training directory..."
if [ -d "ai-training/scripts" ]; then
    echo "✅ AI training scripts preserved (needed for training)"
fi

echo ""
echo "🎉 Cleanup complete!"
echo ""
echo "Files kept (important for production):"
echo "  ✅ Fine_tune_Gikuyu_Mwalimu.ipynb"
echo "  ✅ GIKUYU_MWALIMU_README.md"
echo "  ✅ GIKUYU_IMPLEMENTATION_SUMMARY.md"
echo "  ✅ QUICK_START_CHECKLIST.md"
echo "  ✅ CBC_AGENT_README.md"
echo "  ✅ AI_ARCHITECTURE_PLAN.md"
echo "  ✅ AGENTS.md"
echo "  ✅ deployment/"
echo "  ✅ studio/src/ai/clients/gikuyu-mwalimu-client.ts"
echo "  ✅ .kiro/specs/"
echo ""
echo "Ready to commit and push to GitHub!"
