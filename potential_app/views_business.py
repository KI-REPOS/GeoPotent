from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import UserProfile, Land, Proposal, Bond
from django.contrib.auth.models import User

class BuilderListView(View):
    def get(self, request):
        builders = UserProfile.objects.filter(role='builder')
        return render(request, 'potential_app/builder_list.html', {'builders': builders})

class SubmitProposalView(LoginRequiredMixin, View):
    def get(self, request, builder_id):
        builder = get_object_or_404(User, id=builder_id)
        # Get current user's lands
        lands = Land.objects.filter(owner=request.user)
        return render(request, 'potential_app/submit_proposal.html', {'builder': builder, 'lands': lands})

    def post(self, request, builder_id):
        builder = get_object_or_404(User, id=builder_id)
        land_id = request.POST.get('land_id')
        description = request.POST.get('description')
        
        land = get_object_or_404(Land, id=land_id, owner=request.user)
        
        Proposal.objects.create(
            builder=builder,
            land=land,
            description=description,
            status='pending'
        )
        messages.success(request, f"Proposal sent to {builder.username}!")
        return redirect('dashboard')

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        context = {
            'user_profile': user_profile,
        }
        
        if user_profile.role == 'builder':
            # Proposals received
            proposals = Proposal.objects.filter(builder=request.user).order_by('-created_at')
            context['proposals'] = proposals
            return render(request, 'potential_app/dashboard_builder.html', context)
        else:
            # Proposals sent
            # We need to find proposals where the land belongs to the user
            # But Proposal has 'land' FK, and Land has 'owner' FK.
            # Wait, Proposal.builder is the recipient.
            # Proposal.land.owner is the sender.
            
            # Actually, my model said:
            # builder = ForeignKey(User, related_name='proposals_sent') -- wait, if Landowner sends to Builder, 
            # then 'builder' field should be the Target Builder.
            # My model naming was `builder = ForeignKey(User, related_name='proposals_sent')`. 
            # If the Builder *sends* the proposal, that makes sense.
            # But here Landowner sends to Builder.
            # So `builder` field is the Recipient.
            # `land.owner` is the Sender.
            
            # Let's check my model definition in step 35:
            # builder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals_sent')
            # land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='proposals')
            
            # If Landowner initiates, they are creating a Proposal *for* a Builder.
            # So `builder` is the person who receives it.
            # `related_name='proposals_sent'` is confusing if it's received.
            # I'll assume `builder` is the target.
            
            my_lands = Land.objects.filter(owner=request.user)
            proposals = Proposal.objects.filter(land__in=my_lands).order_by('-created_at')
            context['proposals'] = proposals
            context['lands'] = my_lands
            return render(request, 'potential_app/dashboard_landowner.html', context)

class ProposalDetailView(LoginRequiredMixin, View):
    def get(self, request, proposal_id):
        proposal = get_object_or_404(Proposal, id=proposal_id)
        
        # Security check
        if request.user != proposal.builder and request.user != proposal.land.owner:
            return redirect('dashboard')
            
        return render(request, 'potential_app/proposal_detail.html', {'proposal': proposal})

    def post(self, request, proposal_id):
        # Only builder can accept/reject/upload bond
        proposal = get_object_or_404(Proposal, id=proposal_id)
        if request.user != proposal.builder:
            return redirect('dashboard')
            
        action = request.POST.get('action')
        if action == 'accept':
            proposal.status = 'accepted'
            proposal.save()
        elif action == 'reject':
            proposal.status = 'rejected'
            proposal.save()
        elif action == 'upload_bond':
            # Handle file upload
            if 'bond_file' in request.FILES:
                Bond.objects.create(
                    proposal=proposal,
                    final_agreement=request.FILES['bond_file']
                )
                messages.success(request, "Bond uploaded successfully!")
        
        return redirect('proposal_detail', proposal_id=proposal.id)
