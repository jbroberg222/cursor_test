#!/bin/bash

# Setup script for pre-commit hooks
# Usage: ./setup-pre-commit.sh [basic|advanced|disable]

HOOK_DIR=".git/hooks"
BASIC_HOOK="$HOOK_DIR/pre-commit"
ADVANCED_HOOK="$HOOK_DIR/pre-commit-advanced"
CONFIG_FILE="$HOOK_DIR/pre-commit-config"

echo "🔧 Pre-commit Hook Setup"
echo "========================"

case "${1:-basic}" in
    "basic")
        echo "Setting up basic pre-commit hook..."
        if [ -f "$BASIC_HOOK" ]; then
            cp "$BASIC_HOOK" "$HOOK_DIR/pre-commit"
            chmod +x "$HOOK_DIR/pre-commit"
            echo "✅ Basic pre-commit hook activated"
            echo "   - Runs unit tests before each commit"
            echo "   - Blocks commit if >10% of tests fail"
        else
            echo "❌ Basic hook file not found"
            exit 1
        fi
        ;;
    "advanced")
        echo "Setting up advanced pre-commit hook..."
        if [ -f "$ADVANCED_HOOK" ]; then
            cp "$ADVANCED_HOOK" "$HOOK_DIR/pre-commit"
            chmod +x "$HOOK_DIR/pre-commit"
            echo "✅ Advanced pre-commit hook activated"
            echo "   - Runs unit tests with coverage"
            echo "   - Blocks commit if >10% of tests fail"
            echo "   - Warns if coverage <80%"
        else
            echo "❌ Advanced hook file not found"
            exit 1
        fi
        ;;
    "disable")
        echo "Disabling pre-commit hook..."
        if [ -f "$HOOK_DIR/pre-commit" ]; then
            mv "$HOOK_DIR/pre-commit" "$HOOK_DIR/pre-commit.disabled"
            echo "✅ Pre-commit hook disabled"
            echo "   - Renamed to pre-commit.disabled"
            echo "   - To re-enable: ./setup-pre-commit.sh basic"
        else
            echo "ℹ️  No active pre-commit hook found"
        fi
        ;;
    "status")
        echo "Pre-commit hook status:"
        if [ -f "$HOOK_DIR/pre-commit" ]; then
            echo "✅ Active hook: $(basename $(readlink -f $HOOK_DIR/pre-commit) 2>/dev/null || echo 'pre-commit')"
        elif [ -f "$HOOK_DIR/pre-commit.disabled" ]; then
            echo "❌ Hook disabled: pre-commit.disabled"
        else
            echo "❌ No hook configured"
        fi
        ;;
    *)
        echo "Usage: $0 [basic|advanced|disable|status]"
        echo ""
        echo "Options:"
        echo "  basic    - Basic hook (tests only, 10% failure threshold)"
        echo "  advanced - Advanced hook (tests + coverage, 10% failure + 80% coverage)"
        echo "  disable  - Disable pre-commit hook"
        echo "  status   - Show current hook status"
        echo ""
        echo "Default: basic"
        exit 1
        ;;
esac

echo "========================"
